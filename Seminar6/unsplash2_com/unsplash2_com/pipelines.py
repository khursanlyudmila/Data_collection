# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

# from itemadapter import ItemAdapter


# class Unsplash2ComPipeline:
#    def process_item(self, item, spider):
#        return item

from itemadapter import ItemAdapter
import hashlib
from scrapy.pipelines.images import ImagesPipeline

class CustomImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(request.url.encode()).hexdigest()
        return f"{item['name_image'][0].replace(' ','_')}-{image_guid}.jpg"
    