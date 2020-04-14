# -*- coding: utf-8 -*-
import scrapy
# 导入items.py中的类,为了给定义的数据结构赋值
from ..items import MaoyanItem


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan2'
    allowed_domains = ['maoyan.com']
    url = 'https://maoyan.com/board/4?offset={}'

    # 重写start_requests()方法
    def start_requests(self):
        for offset in range(0, 90, 10):
            url = self.url.format(offset)
            # 交给调度器入队列
            yield scrapy.Request(url=url, callback=self.parse_html)

    def parse_html(self, response):
        dd_list = response.xpath('//dl[@class="board-wrapper"]/dd')
        item = MaoyanItem()
        for dd in dd_list:
            # xpath             :[<selecot xpath='' data='One'>,<selecot xpath='' data='Two'>]
            # 1.extract()       :['One','Two']
            # 2.extract_first() :'One'
            # get()             :'One'
            item["name"] = dd.xpath('./a/@title').get()
            item["star"] = dd.xpath('.//p[@class="star"]/text()').get()
            item["time"] = dd.xpath('.//p[@class="releasetime"]/text()').get()

            # 交给管道文件pipelinses.py处理
            yield item
