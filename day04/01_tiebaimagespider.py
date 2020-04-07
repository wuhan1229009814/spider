"""
爬取指定贴吧的所有图片
"""
import requests
from lxml import etree
import time
import random
from urllib import parse


class TiebaImageSpider:
    def __init__(self):
        self.one_url = "http://tieba.baidu.com/f?kw={}&pn={}"
        # 使用TE的User-Agent
        self.headers = {
            "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)"}

    # 功能函数1 - 请求(获取html)
    def get_html(self, url):
        html = requests.get(url=url, headers=self.headers).text
        return html

    # 功能函数2 - 解析(获取提取结果列表)
    def xpath_html(self, html, xpath_bds):
        p = etree.HTML(html)
        r_list = p.xpath(xpath_bds)
        return r_list

    # 主体逻辑函数 - 主线函数
    def parse_html(self, one_url):
        one_html = self.get_html(url=one_url)
        one_xpath = '//div[@class="t_con cleafix"]/div/div/div/a/@href'
        href_list = self.xpath_html(one_html, one_xpath)
        for href in href_list:
            # 把一个帖子中所有的图片或视频保存到本地
            href_link = 'http://tieba.baidu.com' + href
            self.save_image(href_link)

    # 把一个帖子中所有的图片或视频保存到本地
    def save_image(self, href_link):
        two_html = self.get_html(href_link)
        two_xpath = '//div[@class="d_post_content j_d_post_content  clearfix"]/img[@class="BDE_Image"]/@src | //div[@class="video_src_wrapper"]/embed/@data-video'
        src_list = self.xpath_html(two_html, two_xpath)
        for src in src_list:
            self.write_image(src)
            # 控制爬取速度
            time.sleep(random.uniform(0, 1))

    # 把一张图片或视频保存到本地
    def write_image(self, src):
        img_html = requests.get(url=src, headers=self.headers).content
        filename = src[-10:]
        with open(filename, 'wb') as f:
            f.write(img_html)
        print("%s下载成功" % filename)

    # 入口函数
    def run(self):
        name = input("请输入贴吧名:")
        start_index = int(input("请输入起始页:"))
        end_index = int(input("请输入终止页:"))
        # 对name进行编码
        params = parse.quote(name)
        for page in range(start_index, end_index+1):
            pn = (page-1)*50
            url = self.one_url.format(params, pn)
            self.parse_html(url)


if __name__ == '__main__':
    spider = TiebaImageSpider()
    spider.run()
