'''
Урок 4. Парсинг HTML. XPath

Выберите веб-сайт с табличными данными, который вас интересует.
Напишите код Python, использующий библиотеку requests для отправки HTTP GET-запроса на сайт и получения HTML-содержимого страницы.
Выполните парсинг содержимого HTML с помощью библиотеки lxml, чтобы извлечь данные из таблицы.
Сохраните извлеченные данные в CSV-файл с помощью модуля csv.

Ваш код должен включать следующее:

Строку агента пользователя в заголовке HTTP-запроса, чтобы имитировать веб-браузер и избежать блокировки сервером.
Выражения XPath для выбора элементов данных таблицы и извлечения их содержимого.
Обработка ошибок для случаев, когда данные не имеют ожидаемого формата.
Комментарии для объяснения цели и логики кода.

Примечание: Пожалуйста, не забывайте соблюдать этические и юридические нормы при веб-скреппинге.
'''

# Подключаем библиотеки
import requests
from lxml import html
import pandas as pd
import csv

# Подключаемся к сайту
def get_response():
    url = "https://finance.yahoo.com/trending-tickers/"
    # UserAgent
    headers={
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f'Error response: {url}: {e}')

'''
url = "https://finance.yahoo.com/trending-tickers/"
response = requests.get(url, headers={
    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'})
'''
# Парсинг данных с сайта
def get_data(response):
    tree = html.fromstring(response.content)
    table_rows = tree.xpath("//*[@id='list-res-table']/div[1]/table/tbody/tr")
    all_data = []
    try:
        for row in table_rows:
            columns = row.xpath(".//td/text()")
            data = {
                'Symbol': row.xpath(".//td/a/text()")[0].strip(),
                'Name': columns[0].strip(),
                'Last_Price': row.xpath(".//td/fin-streamer/text()")[0].strip(),
                'Market_Time': row.xpath(".//td/fin-streamer/text()")[1].strip(),
                'Change': row.xpath(".//td/fin-streamer/span/text()")[0].strip(),
                '%_Change': row.xpath(".//td/fin-streamer/span/text()")[1].strip(),
                'Volume': row.xpath(".//td/fin-streamer/text()")[2].strip(),
                'Market_Cap': row.xpath(".//td[8]/fin-streamer/text()[1]"), # Так и не смогла распаковать список из-за исключений - по отдельным строкам есть пустые списки!
                #'Market_Cap': row.xpath(".//td[8]/fin-streamer/text()").strip(),
                #'Market_Cap1': row.xpath(".//td[8]/fin-streamer/text()")[1].strip() if row.xpath(".//td[8]/fin-streamer/text()")[1] else '',
                #'Market_Cap1': row.xpath(".//td[8]/fin-streamer/text()")[1] if row.xpath(".//td[8]/fin-streamer/text()")[0] else '',
                #'Market_Cap': row.xpath(".//td/fin-streamer/text()")[3].strip() if row.xpath(".//td/fin-streamer/text()")[3] else '',
                
            }
            all_data.append(data)
        return all_data
    except Exception as e:
        print(f'Parsing error: {e}')

# Сохранение данных в csv
def save_data(all_data, file_path):
    try:
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            csvwriter = csv.writer(file)
            # Создание заголовков для CSV файла
            for row in all_data:
                csvwriter.writerow([row['Symbol'], row['Name'], row['Last_Price'], row['Market_Time'], row['Change'], row['%_Change'], row['Volume'], row['Market_Cap']])
    except IOError as e:
        print(f'Error save: {file_path}:  {e}')

# Главная функция
def main():
    file_path = 'Seminar4/finance_yahoo.csv'
    response = get_response()
    all_data = get_data(response)  # Получение данных с сайта
    save_data(all_data, file_path)  # Сохранение данных в файл

if __name__ == "__main__":
    main()
