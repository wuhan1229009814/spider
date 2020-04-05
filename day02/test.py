"""
<div class="positionInfo"><span class="positionIcon"></span><a href=".*?" target=".*?" data-log_index=".*?" data-el=".*?">(.*?)</a>.*?<div class="address"><div class="houseInfo"><span class="houseIcon"></span>(.*?)</div>.*?<div class="priceInfo"><div class="totalPrice"><span>(.*?)</span>(.*?)</div>.*?<span>(.*?)</span></div></div>
"""
from urllib import request
import re
import time
import random
from hashlib import md5
import sys
import csv


class LianJiaSpider:
    def __init__(self):
        self.url = "https://wh.lianjia.com/ershoufang/pg{}/"
        self.headers = {"User-Agent": "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50"}

    def get_html(self, url):
        req = request.Request(url=url, headers=self.headers)
        try:
            resp = request.urlopen(req, timeout=3)
            html = resp.read().decode()
            return html
        except Exception as e:
            print(e)

    def regex_func(self, html):
        regex = '<div class="positionInfo"><span class="positionIcon"></span><a href=".*?" target=".*?" data-log_index=".*?" data-el=".*?">(.*?)</a>.*?<div class="address"><div class="houseInfo"><span class="houseIcon"></span>(.*?)</div>.*?<div class="priceInfo"><div class="totalPrice"><span>(.*?)</span>(.*?)</div>.*?<span>(.*?)</span></div></div>'
        pattern = re.compile(regex, re.S)
        r_list = pattern.findall(html)
        return r_list

    def parse_html(self):
        lis = []
        for pg in range(1, 10):
            url = self.url.format(pg)
            html = self.get_html(url)
            r_list = self.regex_func(html)
            for r in r_list:
                tup = (r[0],
                       r[1].split("|")[0],
                       r[1].split("|")[1],
                       r[1].split("|")[2],
                       r[1].split("|")[3],
                       r[1].split("|")[4],
                       r[1].split("|")[5],
                       r[2] + r[3])
                lis.append(tup)
                print(tup)
        with open("fangyuan.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerows(lis)

    def run(self):
        self.parse_html()
        time.sleep(random.randint(1, 2))


if __name__ == '__main__':
    spider = LianJiaSpider()
    spider.run()

