# -*- coding: utf-8 -*-
import scrapy
from ..items import DaomuItem


class DaomuSpider(scrapy.Spider):
    name = 'daomu'
    allowed_domains = ['www.daomubiji.com']
    start_urls = ['http://www.daomubiji.com/']

    # 解析一级页面:提取标题和链接
    def parse(self, response):
        li_list = response.xpath('//li[contains(@id,"menu-item-20")]/a')
        for li in li_list:
            item = DaomuItem()
            item["title"] = li.xpath('./text()').get()
            href = li.xpath('./@href').get()
            # 把所有的href交给调度器入队列
            yield scrapy.Request(
                url=href,
                # meta: 在不同的解析函数之间传递数据
                meta={"item": item},
                callback=self.parse_two_page
            )

    # 二级页面解析函数:卷名+链接
    def parse_two_page(self, response):
        # 拿到上个函数传递过来的item对象
        item = response.meta["item"]

        art_list = response.xpath('//article')
        for art in art_list:
            item["name"] = art.xpath('./a/text()').get()
            link = art.xpath('./a/@href').get()
            # 把章节链接交给调度器入队列
            yield scrapy.Request(
                url=link,
                # meta: 在不同的解析函数之间传递数据
                meta={"item": item},
                callback=self.parse_three_page
            )

    # 三级页面解析函数:提取小说内容
    def parse_three_page(self, response):
        # 接收上个函数传递过来的item对象
        item = response.meta["item"]
        content_list = response.xpath('//article[@class="article-content"]/p/text()').extract()
        item["content"] = "\n".join(content_list)
        yield item
