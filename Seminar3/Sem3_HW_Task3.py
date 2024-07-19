'''
Урок 3. Системы управления базами данных MongoDB и Кликхаус в Python

2. Загрузите данные который вы получили на предыдущем уроке путем скрейпинга сайта
с помощью Buautiful Soup в MongoDB и создайте базу данных и коллекции для их хранения.
3. Поэкспериментируйте с различными методами запросов.
'''

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

# Выбор базы данных и коллекции
db = client['all_books_data']
collection = db['downloaded_books']

# Запрос на поиск количества книг по диапазону цены
query_price = {"Price" : {"$gt" : 50, "$lte" : 100}}
print(f"Количество книг дороже 50, но дешевле 100 фунтов: {collection.count_documents(query_price)}")

# Вывод названий книг
books = collection.find(query_price)
for book in books:
    print("Название книги:", book['Title']+",", "цена книги:", book['Price'])

# Запрос на поиск книг по набору слов в их названиях
query_title = {"Title" : {"$regex" : "[Ss]tory | [Mm]usic"}}
print(f"Количество книг, в названии которых присутствуют слова 'music' или 'story': {collection.count_documents(query_title)}")

# Вывод названий книг
books = collection.find(query_title)
for book in books:
    print("Название книги:", book['Title'])