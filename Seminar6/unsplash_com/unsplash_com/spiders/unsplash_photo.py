'''
Урок 6. Scrapy. Парсинг фото и файлов

1. Создайте новый проект Scrapy. Дайте ему подходящее имя и убедитесь, что ваше окружение правильно
настроено для работы с проектом.
2. Создайте нового паука, способного перемещаться по сайту www.unsplash.com.
Ваш паук должен уметь перемещаться по категориям фотографий и получать доступ к страницам отдельных фотографий.
3. Определите элемент (Item) в Scrapy, который будет представлять изображение.
Ваш элемент должен включать такие детали, как URL изображения, название изображения и категорию,
к которой оно принадлежит.
4. Используйте Scrapy ImagesPipeline для загрузки изображений.
Обязательно установите параметр IMAGES_STORE в файле settings.py.
Убедитесь, что ваш паук правильно выдает элементы изображений, которые может обработать ImagesPipeline.
5. Сохраните дополнительные сведения об изображениях (название, категория) в CSV-файле.
Каждая строка должна соответствовать одному изображению и содержать URL изображения,
локальный путь к файлу (после загрузки), название и категорию.
'''

import scrapy

class UnsplashPhotoSpider(scrapy.Spider):
    name = "unsplash_photo"
    #allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com"]

    def parse(self, response):
        # Проходимся по списку изображений
        for image in response.xpath('//*[@itemprop="contentUrl"]/@href').extract():
            # Соединяем ссылку на полное отдельное  изображение   
            yield scrapy.Request(response.urljoin(image), self.parse_image_page)

    def parse_image_page(self, response):
        image_page_url = response.xpath('//*[@class="wdUrX"]/img[2]/@src').extract_first()
        if image_page_url:
            yield scrapy.Request(response.urljoin(image_page_url), self.save_image)

    def save_image(self, response):
        filename = response.url.split('/')[-1][0:20] + ".jpg"

        with open(f'images/{filename}', 'wb') as f:
            f.write(response.body)
