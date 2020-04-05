"""存CSV文件"""
from urllib import request
import re
import time
import random
import csv


class MaoYanSpider:
    def __init__(self):
        self.url = "https://maoyan.com/board/4?offset={}"
        self.headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E) QQBrowser/6.9.11079.201"}
        # 打开文件,并初始化写入对象
        self.f = open("film.csv", "a")
        self.writer = csv.writer(self.f)

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
        # 数据存入csv文件
        for film in film_list:
            L = [
                film[0].strip(),
                film[1].strip()[3:],
                film[2].strip()[5:15]
            ]
            self.writer.writerow(L)

    def run(self):
        # 入口函数
        for page in range(0, 31, 10):
            url = self.url.format(page)
            self.get_html(url)
            time.sleep(random.randint(1, 2))
        # 所有数据抓取完成后关闭文件
        self.f.close()


if __name__ == '__main__':
    start_time = time.time()
    spider = MaoYanSpider()
    spider.run()
    end_time = time.time()
    print("执行时间:%.2f" % (end_time-start_time))
