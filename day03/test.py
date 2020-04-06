import requests
from lxml import etree
import time
import random


class TiebaSpider:
    def __init__(self):
        self.word = input("请输入贴吧名:")
        self.url = "http://tieba.baidu.com/f?kw={}&pn=50".format(self.word)
        self.headers = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)"}
        self.i = 1

    def parse_html(self):
        # 1.获取响应内容
        url = self.url
        html = requests.get(url=url, headers=self.headers).text
        # 2.提取链接
        p = etree.HTML(html)
        src_list = p.xpath('//div[@class="t_con cleafix"]/div/div/div/a/@href')
        for src in src_list:
            self.save_image(src)
            time.sleep(random.randint(0, 1))

    def save_image(self, src):
        # 保存函数
        url = 'http://tieba.baidu.com{}'.format(src)
        html = requests.get(url=url, headers=self.headers).text
        p = etree.HTML(html)
        # img_list = p.xpath('//div[@class="d_post_content j_d_post_content  clearfix"]/img[@class="BDE_Image"]/@src')
        # for img in img_list:
        #     images = requests.get(url=img, headers=self.headers).content
        #     filename = self.word + "_" + str(self.i) + "." + img.split(".")[-1]
        #     with open(filename, "wb") as f:
        #         f.write(images)
        #     print(filename, "抓取成功")
        #     self.i += 1
        video_list = p.xpath('.//div[@class="video_src_wrapper"]/embed/@data-video')
        if not video_list:
            return
        for video in video_list:
            print(video)
            video = requests.get(url=video, headers=self.headers).content
            name = self.word + "-" + str(self.i) + '.mp4'
            with open(name, "wb+") as f:
                f.write(video)
            print(name, "抓取成功")
            self.i += 1


if __name__ == '__main__':
    spider = TiebaSpider()
    spider.parse_html()







