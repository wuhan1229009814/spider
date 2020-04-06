import requests
from lxml import etree
from fake_useragent import UserAgent
import time
import random


class LianjiaSpider:
    def __init__(self):
        self.url = "https://wh.lianjia.com/ershoufang/pg{}/"

    # 请求功能函数
    def get_html(self, url):
        headers = {"User-Agent": UserAgent().random}
        # 如果某一页有问题,则给3次尝试机会
        for i in range(3):
            try:
                html = requests.get(url=url, headers=headers, timeout=3).text
                self.parse_html(html)
                break
            except Exception as e:
                print(e)

    # 解析功能函数
    def parse_html(self, html):
        p = etree.HTML(html)
        # 1.基准xpath,匹配li节点对象列表
        li_list = p.xpath('//ul[@class="sellListContent"]/li[@class="clear LOGVIEWDATA LOGCLICKDATA"]')
        item = {}
        for li in li_list:
            # 名称 + 区域
            name_list = li.xpath('.//div[@class="positionInfo"]/a[1]/text()')
            item["name"] = name_list[0].strip() if name_list else None
            address_list = li.xpath('.//div[@class="positionInfo"]/a[2]/text()')
            item["address"] = address_list[0].strip() if address_list else None
            # 户型+面积+方位+精装+楼层+年代+类型
            info_list = li.xpath('.//div[@class="houseInfo"]/text()')
            if info_list:
                hlist = info_list[0].split("|")
                item["model"] = hlist[0].strip()
                item["area"] = hlist[1].strip()
                item["direct"] = hlist[2].strip()
                item["perfect"] = hlist[3].strip()
                item["floor"] = hlist[4].strip()
                item["year"] = hlist[5].strip()
                item["type"] = hlist[6].strip()
            else:
                item["model"] = item["area"] = item["direct"] = item["perfect"] = item["floor"] = item["year"] = item[
                    "type"] = None

            # 总价+单价
            total_list = li.xpath('.//div[@class="totalPrice"]/span/text()')
            item["total"] = total_list[0].strip() if total_list else None
            unit_list = li.xpath('.//div[@class="unitPrice"]/span/text()')
            item["unit"] = unit_list[0].strip() if unit_list else None
            print(item)

    def run(self):
        for pg in range(1, 101):
            url = self.url.format(pg)
            self.get_html(url)
            time.sleep(random.randint(1, 2))


if __name__ == '__main__':
    spider = LianjiaSpider()
    spider.run()
