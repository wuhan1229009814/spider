# -*- coding: utf-8 -*-
import scrapy


class TestSpider(scrapy.Spider):
    # 爬虫名
    name = 'test'
    # 允许爬取的域名
    allowed_domains = ['www.test.com']
    # 起始的url地址
    start_urls = ['http://www.test.com/']

    def parse(self, response):
        pass
