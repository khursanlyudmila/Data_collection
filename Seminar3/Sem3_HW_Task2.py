'''
Урок 3. Системы управления базами данных MongoDB и Кликхаус в Python

2. Загрузите данные который вы получили на предыдущем уроке путем скрейпинга сайта
с помощью Buautiful Soup в MongoDB и создайте базу данных и коллекции для их хранения.
3. Поэкспериментируйте с различными методами запросов.
'''

import json
from pymongo import MongoClient

# Подключение к серверу MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Выбор базы данных и коллекции
db = client['all_books_data']
collection = db['downloaded_books']

# Чтение файла
with open("all_books_data.json", 'r', encoding='utf-8') as file:
    try:
        data = json.load(file)
    except Exception as e:
            print(f"Error load data: {e}")

    # Вставляем данные в колекцию
collection.insert_many(data)

print('Data_load')
print(data[0])

# Закрываем соединение с DB
client.close()