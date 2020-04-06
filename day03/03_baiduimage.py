"""
终端输入关键字,抓取图片保存到:/home/tarena/images/关键字/
"""
import requests
import re
import os
import time
import random
from urllib import parse


class BaiduImageSpider:
    def __init__(self):
        self.i = 1
        self.url = "https://image.baidu.com/search/index?tn=baiduimage&word={}"
        self.headers = {"User-Agent": "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50"}
        self.word = input("请输入关键字:")
        self.directory = "/home/tarena/images/{}/".format(self.word)
        # 创建对应的文件夹
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def parse_html(self):
        # 1.获取响应内容
        params = parse.quote(self.word)
        url = self.url.format(params)
        html = requests.get(url=url, headers=self.headers).text
        # 2.提取图片链接
        regex = '"thumbURL":"(.*?)"'
        pattern = re.compile(regex, re.S)
        src_list = pattern.findall(html)
        for src in src_list:
            # 保存图片的函数
            self.save_image(src)
            time.sleep(random.randint(0, 1))

    def save_image(self, src):
        html = requests.get(url=src, headers=self.headers).content
        # filename = self.directory + self.word + "_" + str(self.i) + src.split(".")[-1]
        filename = "{}{}_{}.{}".format(
            self.directory,
            self.word,
            str(self.i),
            src.split(".")[-1]
        )
        with open(filename, "wb") as f:
            f.write(html)
        self.i += 1
        print(filename, "抓取成功")


if __name__ == '__main__':
    spider = BaiduImageSpider()
    spider.parse_html()



