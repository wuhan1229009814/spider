# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DaomuItem(scrapy.Item):
    # define the fields for your item here like:
    # 想一想:在管道文件中数据处理需要什么字段
    # 标题 + 卷名 + 小说内容
    title = scrapy.Field()
    name = scrapy.Field()
    content = scrapy.Field()
