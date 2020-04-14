# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


# 管道1 - 终端打印输出
class MaoyanPipeline(object):
    def process_item(self, item, spider):
        print(item['name'], item['time'], item['star'])
        return item


# 管道2 - 数据存入MySQL
import pymysql
from .settings import *
class MaoyanMysqlPipeline(object):
    # 爬虫程序启动时,只执行1次,一般用于数据库的连接
    def open_spider(self, spider):
        self.db = pymysql.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE,
            charset=CHARSET
        )
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        ins = 'insert into filmtab values(%s,%s,%s)'
        li = [item["name"], item["star"], item["time"]]
        self.cursor.execute(ins, li)
        self.db.commit()
        return item

    # 爬虫程序结束时,只执行1次,一般用于数据库的断开
    def close_spider(self, spider):
        self.cursor.close()
        self.db.close()


# 管道3 - 数据存入mongodb
import pymongo
class MaoyanMongoPipeline(object):
    # 爬虫程序启动时,只执行1次,一般用于数据库的连接
    def open_spider(self, spider):
        self.conn = pymongo.MongoClient(host=MONGO_HOST, port=MONGO_PORT)
        self.db = self.conn[MONGO_DB]
        self.myset = self.db[MONGO_SET]

    def process_item(self, item, spider):
        # 把对象item处理成字典
        film_dict = dict(item)
        # 存入mongodb数据库
        self.myset.insert_one(film_dict)
        # 把process_item()函数的返回值,继续交由下一个管道处理
        return item
