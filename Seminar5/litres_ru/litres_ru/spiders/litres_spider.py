'''
Урок 5. Scrapy

1. Найдите сайт, содержащий интересующий вас список или каталог.
Это может быть список книг, фильмов, спортивных команд или что-то еще, что вас заинтересовало.

2. Создайте новый проект Scrapy и определите нового паука.
С помощью атрибута start_urls укажите URL выбранной вами веб-страницы.

3. Определите метод парсинга для извлечения интересующих вас данных.
Используйте селекторы XPath или CSS для навигации по HTML и извлечения данных.
Возможно, потребуется извлечь данные с нескольких страниц или перейти по ссылкам на другие
страницы.

4. Сохраните извлеченные данные в структурированном формате.
Вы можете использовать оператор yield для возврата данных из паука,
которые Scrapy может записать в файл в выбранном вами формате (например, JSON или CSV).

5. Конечным результатом работы должен быть код Scrapy Spider, а также пример выходных данных.
Не забывайте соблюдать правила robots.txt и условия обслуживания веб-сайта,
а также ответственно подходите к использованию веб-скрейпинга.
'''

import scrapy


class LitresSpiderSpider(scrapy.Spider):
    name = "litres_spider"
    allowed_domains = ["www.litres.ru"]
    start_urls = ["https://www.litres.ru/genre/knigi-ezoterika-5011"]

    def parse(self, response):
        rows = response.xpath('//div[@class="ArtDefault_wrapper__VmWpW ArtDefault_wrapper__adaptive__VW5z0"]')
        for row in rows:
            book_name = row.xpath('.//div[@class="ArtDefault_cover__text__HKF_g"]/div/a/p/text()').get()
            book_author = row.xpath('.//div[@class="ArtDefault_cover__text__HKF_g"]/div/div/a/text()').get()
            book_reader = row.xpath('.//div[@class="ArtDefault_cover__text__HKF_g"]/div/div[2]/a/text()').get()
            book_rating = row.xpath('.//div[@class="ArtDefault_cover__text__HKF_g"]/div[2]/div[2]/div[2]/text()').get()
            book_votes = row.xpath('.//div[@class="ArtDefault_cover__text__HKF_g"]/div[2]/div[2]/div[3]/text()').get()
            link = row.xpath(".//a/@href").get()
            yield response.follow(url=link, callback=self.parse_book,
                                  meta={
                                      'book_name': book_name,
                                      'book_author': book_author,
                                      'book_reader': book_reader,
                                      'book_rating': book_rating,
                                      'book_votes': book_votes,
                                  })
    
    def parse_book(self, response):
        rows = response.xpath('//div[@class="BookCard_book__actionsBlock__ivnYI"]/div')
        for row in rows:
            book_name = response.request.meta['book_name']
            book_author = response.request.meta['book_author']
            book_reader = response.request.meta['book_reader']
            book_rating = response.request.meta['book_rating']
            book_votes = response.request.meta['book_votes']
            book_price_abonement = row.xpath('.//div[1]/div[1]/strong/text()').get()
            book_price_sale = row.xpath('.//div[2]/div[1]/strong/text()').get()
            yield{
                'book_name': book_name,
                'book_author': book_author,
                'book_reader': book_reader,
                'book_rating': book_rating,
                'book_votes': book_votes,
                'book_price_abonement': book_price_abonement.strip() if book_price_abonement else None,
                'book_price_sale': book_price_sale.strip() if book_price_sale else None,
            }

# Запуск паука и сохранение файла по команде в терминале:
# scrapy crawl litres_spider -o litres_books.json