# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os

from .settings import IMAGES_STORE
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

class AnimeimagecrawlPipeline(object):
    def process_item(self, item, spider):
        return item

class AnimePicturesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        self.item = item
        for image_url in item['image_urls']:
            yield Request(image_url, meta={'image_path': item['image_path']})

    def item_completed(self, result, item, info):
        image_path = [x['path'] for ok, x in result if ok]
        if not image_path:
            raise DropItem("Item contain not image")
        item['image_path'] = image_path
        return item
    def file_path(self, request, response=None, info=None):
        return request.meta['image_path']
