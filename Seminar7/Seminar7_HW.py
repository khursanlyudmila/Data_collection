'''
Урок 7. Selenium в Python

1. Выберите веб-сайт, который содержит информацию, представляющую интерес для извлечения данных.
Это может быть новостной сайт, платформа для электронной коммерции или любой другой сайт,
который позволяет осуществлять скрейпинг (убедитесь в соблюдении условий обслуживания сайта).
2. Используя Selenium, напишите сценарий для автоматизации процесса перехода на нужную страницу сайта.
3. Определите элементы HTML, содержащие информацию, которую вы хотите извлечь (например, заголовки статей, названия продуктов, цены и т.д.).
4. Используйте BeautifulSoup для парсинга содержимого HTML и извлечения нужной информации из идентифицированных элементов.
5. Обработайте любые ошибки или исключения, которые могут возникнуть в процессе скрейпинга.
6. Протестируйте свой скрипт на различных сценариях, чтобы убедиться, что он точно извлекает нужные данные.
7. Предоставьте ваш Python-скрипт вместе с кратким отчетом (не более 1 страницы), который включает следующее: URL сайта.
Укажите URL сайта, который вы выбрали для анализа. Описание. Предоставьте краткое описание информации,
которую вы хотели извлечь из сайта.
Подход. Объясните подход, который вы использовали для навигации по сайту,
определения соответствующих элементов и извлечения нужных данных.
Трудности. Опишите все проблемы и препятствия, с которыми вы столкнулись в ходе реализации проекта, и как вы их преодолели.
Результаты. Включите образец извлеченных данных в выбранном вами структурированном формате (например, CSV или JSON).
Примечание: Обязательно соблюдайте условия обслуживания сайта и избегайте чрезмерного скрейпинга, который может нарушить нормальную работу сайта.
'''

import csv

from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

from selenium.webdriver.support.ui import WebDriverWait # Модуль для ожидания наступления определенного условия
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.ui import Select

from selenium.common.exceptions import TimeoutException, NoSuchElementException # Отлов ошибок

import requests
from bs4 import BeautifulSoup

user_agent = (
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
)
url = 'https://www.chitai-gorod.ru/'
chrome_option = Options()
chrome_option.add_argument(f'user-agent={user_agent}')
driver = webdriver.Chrome(options=chrome_option)

# Переход на первую страницу веб-сайта
driver.get(url)

# Таймер задержки
time.sleep(4)

# Определение строки поиска и ввод запроса в поисковую строку
wait = WebDriverWait(driver, 5) # Ожидание прогрузки страницы
search_box = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@class='header-search__input']"))) # Ищем строку поиска

# Вводим фразу поиска и нажимаем Enter
search_box.send_keys('менегетти антонио') # Имитируем ввод запроса в строку поиска
search_box.send_keys(Keys.ENTER) # Имитируем нажание кнопки ввода

# Обработка запроса Cookie
wait = WebDriverWait(driver, 5)
cookie_box = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@class='button cookie-notice__button white']")))
cookie_box.send_keys(Keys.ENTER)

# Модуль создания списка, прокручивания сайта и подсчёта книг, парсинга и перехода на следующию страницу
book_list = [] # Список книг
# Прокручиваем сайт до конца
try:
    while True:
        count = None # Для подсчёта карточек книг
        while True:
            time.sleep(4) # Таймер задержки
            books = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='products-list']/article"))) # Ищем карточку книги
            
            if len(books) == count: # Выходим из цикла, если при прокрутке страницы, количество карточек книг не меняется
                break

            count = len(books) # Посчитываем количество книг на странице
            
            driver.execute_script('window.scrollBy(0, 1800)') # Прокручиваем страницу выполняя JAVA Script
            time.sleep(2) # Таймер задержки
        # Проходимся по карточкам, извлекаем ссылку на книгу и добавляем в book_list    
        for book in books:
            book_name = book.find_element(By.XPATH, './a[1]').get_attribute('title')
            book_old_price = book.get_attribute('data-chg-product-old-price')
            book_price = book.get_attribute('data-chg-product-price')
            
            sale_status = book.get_attribute('data-chg-product-status')
            #if sale_status == 'canBuy':
            #    sale_status == 'Можно купить'
            #    if sale_status == 'canSubscribe':
            #        sale_status == 'Зарезервировать'
            #        if sale_status == 'offline':
            #            sale_status == 'Не продается'
            
            # Пример обработки исключения на элементе "review_count"
            try:       
                review_count = book.find_element(By.XPATH, './a[2]/div/div/div[2]/meta[3]').get_attribute('content')
            except (TimeoutException, Exception):
                review_count = None

            # Парсинг дополнительного элемента (Количестов бонусных рублей) с помощью BeautifulSoup
            url_item = book_list
            response = driver.page_source
            soup = BeautifulSoup(response, features="html.parser")
            product_offer_bonus = soup.find("span", class_="product-offer-bonus__text")
            
            try:
                book_offer_bonus = product_offer_bonus.text()
                
            except (TimeoutException, Exception):
               book_offer_bonus = None

            url = book.find_element(By.XPATH, './a[1]').get_attribute('href')
            book_list.append({
                'book_name': book_name,
                'book_old_price': book_old_price,
                'book_price': book_price,
                'sale_status': sale_status,
                'review_count': review_count,
                'product_offer_bonus': product_offer_bonus,
                'url_book': url, 
                })
            #print(book_list)
        
        # Проверка наличия следующей кнопки
        #next_button = driver.find_elements(By.XPATH, '//li[@class="pagination__wrapper"]/a')
        #if not next_button:
        #    break
        # Нажатие следующей кнопки
        #next_button[0].click()
        # Ожидание загрузки страницы
        #time.sleep(5)

        next_button_locator = (By.XPATH, '//li[@class="pagination__wrapper"]/a[3]')  # тег для поиска ссылки на следующую страницу

        current_page = 1
        while True:
            print(f"Scraping page {current_page}...")
            try:
                next_button = driver.find_element(*next_button_locator)
                next_button.click()
                current_page += 1
            except NoSuchElementException:
                break
        break


finally:
    driver.quit()

print(f'Всего получено: {len(book_list)} ссылок на книги')

# Сохранение списка в файл вормата .csv
books_file = 'book_list.csv'
with open(books_file, 'w', newline='', encoding='UTF-8') as f:
    write = csv.DictWriter(f, fieldnames=['book_name', 'book_old_price', 'book_price', 'sale_status', 'review_count', 'product_offer_bonus', 'url_book'])
    write.writeheader()
    write.writerows(book_list)
print(f'Данные успешно сохранены в файл: {books_file}')
