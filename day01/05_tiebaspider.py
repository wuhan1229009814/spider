from urllib import request, parse
import time
import random


class TiebaSpider:
    def __init__(self):
        """定义常用变量"""
        self.url = "http://tieba.baidu.com/f?kw={}&pn={}"
        self.headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0)"}

    # 请求
    def get_html(self, url):
        req = request.Request(url=url, headers=self.headers)
        resp = request.urlopen(req)
        html = resp.read().decode()
        return html

    # 解析
    def parse_html(self):
        pass

    # 保存
    def save_html(self, filename, html):
        with open(filename, "w") as f:
            f.write(html)

    # 入口函数
    def run(self):
        name = input("请输入贴吧名:")
        begin_index = int(input("请输入起始页"))
        end_index = int(input("请输入终止页"))
        params = parse.quote(name)
        for page in range(begin_index, end_index+1):
            # 拼接URL地址, 发请求,获取响应,最终保存
            pn = (page - 1) * 50
            url = self.url.format(params, pn)
            html = self.get_html(url)
            filename = "{}_第{}页.html".format(name, page)
            self.save_html(filename, html)
            time.sleep(random.randint(1, 2))
            print("第{}页抓取成功".format(page))


if __name__ == '__main__':
    spider = TiebaSpider()
    spider.run()













