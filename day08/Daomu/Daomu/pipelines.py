# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
class DaomuPipeline(object):
    def process_item(self, item, spider):
        # /home/tarena/daomu/盗墓笔记1-xxx/七星鲁王_第一章_血尸.txt
        directory = '/home/tarena/daomu/{}/'.format(item["title"])
        if not os.path.exists(directory):
            os.makedirs(directory)
        # 写入文件
        filename = directory + item["name"].replace(" ", "_") + ".txt"
        with open(filename, "w") as f:
            f.write(item["content"])
        return item
