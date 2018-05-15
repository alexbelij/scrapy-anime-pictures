# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AnimeimagecrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class AnimePicturesItem(scrapy.Item):
    title = scrapy.Field()
    image_urls = scrapy.Field()
    image_path = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
