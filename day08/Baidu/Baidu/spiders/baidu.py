# -*- coding: utf-8 -*-
import scrapy


class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['wwww.baidu.com']
    start_urls = ['http://wwww.baidu.com/']

    # response:http://wwww.baidu.com/ 的响应对象
    def parse(self, response):
        r_list = response.xpath('/html/head/title/text()')
        print("*"*50)
        print(r_list)










