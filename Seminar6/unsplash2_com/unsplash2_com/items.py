# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

# import scrapy


# class Unsplash2ComItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass

import scrapy
#from scrapy.item import Item, Field

class UnsplashImgItem(scrapy.Item):
    name_image = scrapy.Field()
    category_image = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()