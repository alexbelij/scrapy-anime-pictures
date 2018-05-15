# -*- coding: utf-8 -*-
import scrapy
import re
import codecs
from ..settings import IMAGES_STORE
from ..items import AnimePicturesItem
from configparser import ConfigParser

import os

config = ConfigParser()
config.readfp(codecs.open('setting.ini', 'r', encoding='utf-8-sig'))
class AnimesPictures(scrapy.Spider):
    """
        Crawl Image form https://anime-pictures.net
        If you want to search tags, please modify setting.ini
        I recommand search tag by English.
    """

    name = 'AnimePictures'
    start_urls = ['https://anime-pictures.net']

    def __init__(self):
        self.tags = config.get('IMG', 'tags').strip().split('\n')
        self.account = config.get('LOGIN', 'account')
        self.password = config.get('LOGIN', 'password')

        self.cookie = {
                '__cfduid': 'dc82ef0da540ca28afb227e6eddbd227f1525854296',
                '_ga': 'GA1.2.920944478.1525854226',
                'caltat': 'cb287303cea4464a882ab0232fca1ab4',
                '_gid': 'GA1.2.635646527.1526285102',
                'sitetheme': 'first',
                'time_zone': 'Asia/Shanghai',
                'asian_server': '069cfdb6ea4743c28c66ae94b3100577',
                'sitelang': 'jp'
        }

    def start_requests(self):
        if not self.account or not self.password:
            callback = self.search_tags
        else:
            callback = self.login
        return [scrapy.Request(
                    self.start_urls[0],
                    callback=callback
                )]

    def login(self, response):
        formdata = {
            'login': self.account,
            'password': self.password,
            'time_zone': 'Asia/Shanghai'
        }
        return scrapy.FormRequest(
                self.start_urls[0] + '/login/submit',
                cookies=self.cookie,
                formdata=formdata,
                callback=self.search_tags
                )

    def search_tags(self, response):
        for tag in self.tags:
            url = 'https://anime-pictures.net/pictures/view_posts/0?search_tag=%s&lang=jp' %tag
            yield scrapy.Request(
                    url,
                    cookies=self.cookie,
                    callback=self.image_page
                    )

    def image_page(self, response):
        next_page = response.css('.numeric_pages *')[-1]\
                            .css('a::attr("href")').extract_first()
        if not not next_page:
            yield scrapy.Request(
                    self.start_urls[0] + next_page,
                    cookies=self.cookie,
                    callback=self.image_page
                    )
        #scrapy.utils.response.open_in_browser(response)
        urls = response.css('span.img_block_big > a:first-of-type::attr("href")').extract()
        for url in urls:
            yield scrapy.Request(
                    self.start_urls[0] + url,
                    cookies=self.cookie,
                    callback=self.parse_detail
                    )

    def parse_detail(self, response):
        title = 'No' + re.search(
                           r'\d+',
                           response.css('.post_content h1::text')\
                                   .extract_first()
                       ).group()
        image_url = 'http:' + response.css('img#big_preview::attr("src")')\
                                    .extract_first()
        author = response.css('.tags li.orange a::text')\
                         .extract_first()
        tags = response.css('.tags li[class=""] a::text')\
                       .extract()
        item = AnimePicturesItem()
        item['title'] = title
        item['image_urls'] = [image_url]
        item['author'] = author or 'other'
        item['image_path'] = '/%s/%s.jpg' %(item['author'], item['title'])
        if os.path.isfile(IMAGES_STORE + item['image_path']):
            return
        #item['tags'] = tags
        return item

