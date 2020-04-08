"""
民政部网站最新行政区划代码抓取 - 增量
"""
import requests
from lxml import etree
from fake_useragent import UserAgent
import re
import pymysql
from hashlib import md5


class MzbSpider:
    def __init__(self):
        self.url = 'http://www.mca.gov.cn/article/sj/xzqh/2019/'
        self.headers = {"User-Agent": UserAgent().random}
        self.db = pymysql.connect(
            "localhost", "root", "123456", "mzbdb", charset="utf8"
        )
        self.cursor = self.db.cursor()
        # 创建3个空列表,用于excutemny()批量插入表记录
        self.province_list = []
        self.city_list = []
        self.county_list = []

    # 请求函数
    def get_html(self, url):
        html = requests.get(url=url, headers=self.headers).text
        return html

    # 解析函数
    def xpath_func(self, html, xpath_bds):
        p = etree.HTML(html)
        r_list = p.xpath(xpath_bds)
        return r_list

    # 主体逻辑函数
    def get_link(self):
        one_html = self.get_html(url=self.url)
        xpath_bds = '//table//tr[2]/td[2]/a/@href'
        href_lsit = self.xpath_func(one_html, xpath_bds)
        if href_lsit:
            link = 'http://www.mca.gov.cn' + href_lsit[0]
            s = md5()
            s.update(link.encode())
            finger = s.hexdigest()
            sel = 'select * from request_finger where finger=%s'
            result = self.cursor.execute(sel, [finger])
            if not result:
                # 提取数据函数
                self.get_data(link)
                # 把指纹存入指纹表
                ins = 'insert into request_finger values(%s)'
                self.cursor.execute(ins, [finger])
                self.db.commit()
                self.cursor.close()
                self.db.close()
            else:
                print("更新完成")
        else:
            print("链接提取失败")

    # 提取数据函数
    def get_data(self, link):
        two_html = self.get_html(link)
        # 在two_html中提取真实链接
        regex = r'window.location.href="(.*?)"'
        patern = re.compile(regex, re.S)
        real_link_list = patern.findall(two_html)
        if real_link_list:
            real_link = real_link_list[0]
            # 向真实链接发请求,提取最终数据
            self.parse_html(real_link)
        else:
            print("提取真实链接失败")

    # 提取真实数据
    def parse_html(self, real_link):
        real_html = self.get_html(real_link)
        real_xpath = '//tr[@height=19]'
        tr_list = self.xpath_func(real_html, real_xpath)
        for tr in tr_list:
            name_list = tr.xpath('./td[3]/text()')
            code_list = tr.xpath('./td[2]/text()')
            if name_list and code_list:
                name = name_list[0].strip()
                code = code_list[0].strip()
                print(name, code)
                # 判断name是 省 市 县
                if code[-4:] == "0000":
                    self.province_list.append((name, code))
                    # 把4个直辖市加入市表
                    if name in ["北京市", "天津市", "上海市", "重庆市"]:
                        self.city_list.append((name, code, code))
                elif code[-2:] == "00":
                    self.city_list.append((name, code, code[:2]+"0000"))
                else:
                    if code[:2] in ["11", "12", "31", "50"]:
                        xfather_code = code[:2] + "0000"
                    else:
                        xfather_code = code[:4] + "00"
                    self.county_list.append((name, code, xfather_code))
        # 存入数据库
        self.insert_mysql()

    # 数据存入数据库
    def insert_mysql(self):
        # 1.首先清空数据库
        del1 = 'delete from province'
        del2 = 'delete from city'
        del3 = 'delete from county'
        self.cursor.execute(del1)
        self.cursor.execute(del2)
        self.cursor.execute(del3)
        # 2.存入数据库
        ins1 = 'insert into province values(%s,%s)'
        ins2 = 'insert into  city values(%s,%s,%s)'
        ins3 = 'insert into county values(%s,%s,%s)'
        self.cursor.executemany(ins1, self.province_list)
        self.cursor.executemany(ins2, self.city_list)
        self.cursor.executemany(ins3, self.county_list)
        self.db.commit()

    # 入口函数
    def run(self):
        self.get_link()


if __name__ == '__main__':
    spider = MzbSpider()
    spider.run()
