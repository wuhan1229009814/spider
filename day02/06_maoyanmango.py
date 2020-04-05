from urllib import request
import re
import pymongo
import time
import random


class MaoYanSpider:
    def __init__(self):
        self.url = "https://maoyan.com/board/4?offset={}"
        self.headers = {"User-Agent": "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50"}
        self.conn = pymongo.MongoClient("localhost", 27017)
        self.db = self.conn["maoyandb"]
        self.myset = self.db["maoyanset"]

    def get_html(self, url):
        req = request.Request(url=url, headers=self.headers)
        resp = request.urlopen(req)
        html = resp.read().decode()
        # 直接调用解析函数
        self.pares_html(html)

    def pares_html(self, html):
        # 解析
        regex = '<div class="movie-item-info">.*?title="(.*?)".*?<p class="star">(.*?)</p>.*?<p class="releasetime">(.*?)</p>'
        pattern = re.compile(regex, re.S)
        film_list = pattern.findall(html)
        # 直接调用解析函数
        self.save_html(film_list)

    def save_html(self, film_list):
        # 保存
        for film in film_list:
            item = {}
            item["name"] = film[0].strip()
            item["star"] = film[1].strip()[3:]
            item["time"] = film[2].strip()[5:15]
            print(item)
            # 把数据存入到mangodb数据库
            self.myset.insert_one(item)

    def run(self):
        # 入口函数
        for page in range(0, 31, 10):
            url = self.url.format(page)
            self.get_html(url)
            time.sleep(random.randint(1, 2))


if __name__ == '__main__':
    start_time = time.time()
    spider = MaoYanSpider()
    spider.run()
    end_time = time.time()
    print("执行时间:%.2f" % (end_time - start_time))
