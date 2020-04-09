"""
腾讯招聘指定岗位信息抓取
"""
import requests
import json
from threading import Thread, Lock
from queue import Queue
from urllib import parse
import time
from fake_useragent import UserAgent


class TencentSpider:
    def __init__(self):
        self.one_url = 'https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1563912271089&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword={}&pageIndex={}&pageSize=10&language=zh-cn&area=cn'
        self.two_url = 'https://careers.tencent.com/tencentcareer/api/post/ByPostId?timestamp=1563912374645&postId={}&language=zh-cn'
        self.one_q = Queue()
        self.two_q = Queue()
        self.headers = {"User-Agent": UserAgent().random}
        # 存入json文件
        self.f = open("tencent.json", "w")
        self.job_info_list = []
        self.i = 0
        self.lock = Lock()

    # URL入队列
    def url_in(self):
        keyword = input("请输入职位类别:")
        keyword = parse.quote(keyword)
        # 获取某个职位类别的总页数
        total = self.get_total(keyword)
        for page in range(1, total):
            one_url = self.one_url.format(keyword, page)
            self.one_q.put(one_url)

    # 获取某个职位类别的总页数
    def get_total(self, kerword):
        url = self.one_url.format(kerword, 1)
        html = requests.get(url=url, headers=self.headers).json()
        count = html["Data"]["Count"]
        if count % 10 == 0:
            total = count // 10 + 1
        else:
            total = count // 10 + 2
        return total

    # 一级页面线程事件函数
    def parse_one_page(self):
        while not self.one_q.empty():
            one_url = self.one_q.get()
            one_html = requests.get(url=one_url, headers=self.headers).json()
            for one_job in one_html["Data"]["Posts"]:
                # 提取postid + 拼接职位详情页的链接
                postid = one_job["PostId"]
                two_url = self.two_url.format(postid)
                # 把详情页的链接put到二级队列中
                self.two_q.put(two_url)

    # 二级页面线程事件函数:提取职位具体信息
    def parse_two_page(self):
        while True:
            try:
                two_url = self.two_q.get(block=True, timeout=3)
                two_html = requests.get(url=two_url, headers=self.headers).json()
                item = {}
                item['job_name'] = two_html["Data"]["RecruitPostName"]
                item['job_adress'] = two_html["Data"]["LocationName"]
                item['job_type'] = two_html["Data"]["CategoryName"]
                item['job_duty'] = two_html["Data"]["Responsibility"]
                item['job_require'] = two_html["Data"]["Requirement"]
                item['job_time'] = two_html["Data"]["LastUpdateTime"]
                print(item)
                self.lock.acquire()
                self.i += 1
                # 存json文件使用
                self.job_info_list.append(item)
                self.lock.release()
            except Exception as e:
                break

    # 入口函数
    def run(self):
        # 1.URL入队列
        self.url_in()
        # 2.创建并启动线程
        t1_list = []
        t2_list = []
        for i in range(2):
            t1 = Thread(target=self.parse_one_page)
            t1_list.append(t1)
            t1.start()
        for i in range(2):
            t2 = Thread(target=self.parse_two_page)
            t2_list.append(t2)
            t2.start()
        for t1 in t1_list:
            t1.join()
        for t2 in t2_list:
            t2.join()
        # 把数据存入json文件
        json.dump(self.job_info_list, self.f, ensure_ascii=False)
        self.f.close()
        print("数量:", self.i)


if __name__ == '__main__':
    start_time = time.time()
    spider = TencentSpider()
    spider.run()
    end_time = time.time()
    print("执行时间:%.2f" % (end_time - start_time))
