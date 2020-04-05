from urllib import request
import re
import time
import random
import pymysql
from hashlib import md5
import pymongo
import sys


class CarSpider:
    def __init__(self):
        self.one_url = "https://www.che168.com/beijing/a0_0msdgscncgpi1lto1csp{}exx0/"
        self.headers = {"User-Agent": "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50"}
        self.db = pymysql.connect(
            "localhost", "root", "123456", "cardb", charset="utf8"
        )
        self.cursor = self.db.cursor()
        # mongodb常用变量
        self.conn = pymongo.MongoClient("localhost", 27017)
        self.mdb = self.conn["cardb"]
        self.myset = self.mdb["carset"]

    # 功能函数1
    def get_html(self, url):
        req = request.Request(url=url, headers=self.headers)
        try:
            resp = request.urlopen(req, timeout=3)
            html = resp.read().decode("gb2312", "ignore")
            return html
        except Exception as e:
            print(e)

    # 功能函数2 - 正则解析
    def regex_func(self, regex, html):
        pattern = re.compile(regex, re.S)
        r_list = pattern.findall(html)
        return r_list

    # 获取数据
    def parse_html(self, one_url):
        one_html = self.get_html(one_url)
        one_regex = '<li class="cards-li list-photo-li".*?<a href="(.*?)".*?</li>'
        # href_list:['/dexxx/xxx/xx','','','',]
        href_list = self.regex_func(one_regex, one_html)
        for href in href_list:
            two_url = "https://www.che168.com" + href
            # 先进行md5加密,因为指纹列表中存储的都是加密后的字符串
            s = md5()
            s.update(two_url.encode())
            finger = s.hexdigest()

            # 指纹表中没有:True,反之返回False
            if self.go_spider(finger):
                # 提取1个汽车的具体数据
                self.get_data(two_url)
                # 爬取1个汽车信息,随机休眠,控制爬取频率
                time.sleep(random.randint(1, 2))
                ins = "insert into request_finger values(%s)"
                self.cursor.execute(ins, [finger])
                self.db.commit()
            else:
                sys.exit("抓取错误")

    # 提取1个汽车的具体数据
    def get_data(self, two_url):
        two_html = self.get_html(two_url)
        two_regex = '<div class="car-box">.*?<h3 class="car-brand-name">(.*?)</h3>.*?<ul class="brand-unit-item fn-clear">.*?<li>.*?<h4>(.*?)</h4>.*?<h4>(.*?)</h4>.*?<h4>(.*?)</h4>.*?<h4>(.*?)</h4>.*?<span class="price" id="overlayPrice">￥(.*?)<b'
        car_list = self.regex_func(two_regex, two_html)
        item = {}
        item["name"] = car_list[0][0].strip()
        item["time"] = car_list[0][1].strip()
        item["km"] = car_list[0][2].strip()
        item["gear"] = car_list[0][3].split("/")[0].strip()
        item["displace"] = car_list[0][3].split("/")[1].strip()
        item["address"] = car_list[0][4].strip()
        item["price"] = car_list[0][5].strip()
        print(item)
        # 存入mangodb
        self.myset.insert_one(item)

    # 程序入口函数
    def run(self):
        for p in range(1, 3):
            url = self.one_url.format(p)
            self.parse_html(url)
        self.cursor.close()
        self.db.close()

    def go_spider(self, finger):
        sel = "select finger from request_finger where finger=%s"
        result = self.cursor.execute(sel, [finger])
        if not result:
            return True
        else:
            return False


if __name__ == '__main__':
    spider = CarSpider()
    spider.run()
