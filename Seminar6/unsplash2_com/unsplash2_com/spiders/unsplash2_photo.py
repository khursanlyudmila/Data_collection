import scrapy

from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose
from ..items import UnsplashImgItem

class Unsplash2PhotoSpider(scrapy.Spider):
    name = "unsplash2_photo"
    #allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com"]

    def parse(self, response):
        for image_page in response.xpath('//*[@itemprop="contentUrl"]/@href').extract():
            yield scrapy.Request(response.urljoin(image_page), self.parse_image_page)

    def parse_image_page(self, response):
        loader = ItemLoader(item=UnsplashImgItem(), response=response)
        loader.default_input_processor = MapCompose(str.strip)
        
        # Название фото
        loader.add_xpath('name_image', '//h1/text()')

        # Парсим категорию картинки
        loader.add_xpath('category_image', '//*[@header="A8yGt"]/h1/text()')

        # Парсим url       
        image_url = response.xpath('//*[@class="wdUrX"]/img[2]/@src').extract_first()
        loader.add_value('image_urls', image_url)

        yield loader.load_item()
