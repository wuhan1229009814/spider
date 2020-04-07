
import time
import requests
from lxml import etree
from fake_useragent import UserAgent
import os


class NoteSpider:
    def __init__(self):
        self.url = 'http://code.tarena.com.cn/AIDCode/aid1909/16_spider/'
        self.directory = '/home/tarena/' + '/'.join(self.url.split("/")[3:])
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        self.auth = ("tarenacode", "code_2014")

    def parse_html(self):
        headers = {"User-Agent": UserAgent().random}
        html = requests.get(url=self.url, auth=self.auth, headers=headers).text
        p = etree.HTML(html)
        href_list = p.xpath('//a[contains(@href, ".zip")]/@href')
        for href in href_list:
            self.download_file(href)

    def download_file(self, href):
        download_url = self.url + href
        headers = {"User-Agent": UserAgent().random}
        download_html = requests.get(url=download_url, auth=self.auth, headers=headers).content
        filename = self.directory + href
        with open(filename, 'wb') as f:
            f.write(download_html)
        print(filename, "下载成功")

    def run(self):
        self.parse_html()


if __name__ == '__main__':
    start_time = time.time()
    spider = NoteSpider()
    spider.run()
    end_time = time.time()
    print("执行时间:%.2f" % (end_time-start_time))
