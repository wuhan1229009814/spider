from urllib import request, parse
import re
import pymysql
import time
import random


class MaoYanSpider:
    def __init__(self):
        self.url = "https://maoyan.com/board/4?offset={}"
        self.headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"}
        self.db = pymysql.connect("localhost", "root", "123456", "mydb", charset="utf8")
        self.cursor = self.db.cursor()

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
        item = {}
        for film in film_list:
            item["name"] = film[0].strip()
            item["star"] = film[1].strip()
            item["time"] = film[2].strip()
            print(item)
            ins = "insert into mytab values(%s,%s,%s)"
            self.cursor.execute(ins, [item['name'], item["star"], item["time"]])
            self.db.commit()

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
    print("执行时间:%.2f" % (end_time-start_time))
