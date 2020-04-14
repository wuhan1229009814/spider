# -*- coding: utf-8 -*-
import scrapy
# 导入items.py中的类,为了给定义的数据结构赋值
from ..items import MaoyanItem


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/board/4?offset=0']
    offset = 0

    def parse(self, response):
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

        # 生成下一页的URL地址交给调度其入队列
        self.offset += 10
        if self.offset <= 90:
            url = 'https://maoyan.com/board/4?offset=' + str(self.offset)
            # 如何把URL交给调度器
            yield scrapy.Request(url=url, callback=self.parse)
