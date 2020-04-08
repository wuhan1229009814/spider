"""
抓取豆瓣电影 - 排行榜 - 所有分类的所有电影
"""
import random
import requests
from fake_useragent import UserAgent
import json
import time
import re


class DoubanSpider:
    def __init__(self):
        self.url = 'https://movie.douban.com/j/chart/top_list?type={}&interval_id=100%3A90&action=&start={}&limit=20'
        # 计数
        self.i = 0

    # 获取html
    def get_html(self, url):
        headers = {"User-Agent": UserAgent().random}
        html = requests.get(url=url, headers=headers).text
        return html

    # 提取数据
    def parse_html(self, url):
        html = json.loads(self.get_html(url))
        item = {}
        for one_film in html:
            item["name"] = one_film["title"]
            item["score"] = one_film["score"]
            item["time"] = one_film["release_date"]
            print(item)
            self.i += 1

    # 入口函数
    def run(self):
        all_type_dict = self.get_all_type_dict()
        menu = ''
        for one in all_type_dict:
            menu = menu + one + '|'
        print(menu)
        choice = input("请选择要抓取电影:")
        # 获取用户输入电影的type的值
        user_type = all_type_dict[choice]
        # total某个类别电影总数
        total = self.get_total(user_type)
        for start in range(0, total, 20):
            url = self.url.format(user_type, start)
            self.parse_html(url)
            # 控制爬取频率
            time.sleep(random.uniform(0, 1))
        print("总数:", self.i)

    # 获取某个类别的电影总数
    def get_total(self, user_type):
        total_url = 'https://movie.douban.com/j/chart/top_list_count?type={}&interval_id=100%3A90'.format(user_type)
        total_html = json.loads(self.get_html(total_url))
        total = total_html['total']
        return total

    def get_all_type_dict(self):
        url = 'https://movie.douban.com/chart'
        html = self.get_html(url)
        regex = '<a href=.*?type_name=(.*?)&type=(.*?)&.*?</a>'
        pattern = re.compile(regex, re.S)
        r_list = pattern.findall(html)
        all_type_dict = {}
        for r in r_list:
            all_type_dict[r[0]] = r[1]
        return all_type_dict


if __name__ == '__main__':
    spider = DoubanSpider()
    spider.run()
