from lxml import etree
from urllib import request
import time
import random


class MaoYanSpider:
    def __init__(self):
        self.url = "https://maoyan.com/board/4?offset={}"
        self.headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"}

    def get_html(self, url):
        req = request.Request(url=url, headers=self.headers)
        resp = request.urlopen(req)
        html = resp.read().decode()
        # 直接调用解析函数
        self.pares_html(html)

    def pares_html(self, html):
        # 1.创建解析对象
        p = etree.HTML(html)
        # 基准xpath: 匹配所有电影信息的节点对象列表
        dd_list = p.xpath('//dl[@class="board-wrapper"]/dd')
        for dd in dd_list:
            itme = {}
            itme["name"] = dd.xpath('.//p[@class="name"]/a/text()')[0].strip()
            itme["star"] = dd.xpath('.//p[@class="star"]/text()')[0].strip()[3:]
            itme["time"] = dd.xpath('.//p[@class="releasetime"]/text()')[0].strip()[5:15]
            print(itme)

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
