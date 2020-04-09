import requests
import json
from multiprocessing import Process, Lock, Queue
import csv
import time
from fake_useragent import UserAgent
import re


class XiaomiSpider:
    def __init__(self):
        self.url = 'http://app.mi.com/categotyAllListApi?page={}&categoryId={}&pageSize=30'
        self.headers = {"User-Agent": UserAgent().random}
        self.q = Queue()
        self.lock = Lock()
        self.i = 0
        # 存入csv文件
        self.f = open('xiaomi.csv', 'w')
        self.weiter = csv.writer(self.f)

    # 获取响应内容
    def get_html(self, url):
        html = requests.get(url=url, headers=self.headers).text
        return html

    # 获取所有分类的ID值
    def get_all_id(self):
        url = 'http://app.mi.com/'
        html = self.get_html(url)
        regex = '<a href="/category/(.*?)"'
        pattern = re.compile(regex, re.S)
        id_list = pattern.findall(html)
        for id in id_list:
            # 每遍历一个分类,将此分类所有页入队列
            self.url_in(id)

    # URL入队列
    def url_in(self, id):
        total = self.get_total(id)
        for page in range(total):
            url = self.url.format(page, id)
            self.q.put(url)

    # 线程事件函数
    def parse_html(self):
        while not self.q.empty():
            time.sleep(0.2)
            url = self.q.get()
            app_list = []
            # 请求 + 解析
            try:
                html = json.loads(self.get_html(url))
                item = {}
                for one_app in html["data"]:
                    item["app_name"] = one_app["displayName"]
                    item["app_type"] = one_app["level1CategoryName"]
                    item["app_link"] = one_app["packageName"]
                    print(item)
                    app_list.append((item["app_name"], item["app_type"], item["app_link"]))
                    # 加锁+释放锁
                    self.lock.acquire()
                    self.i += 1
                    self.lock.release()
                # 把1页的数据写入到csv文件
                self.lock.acquire()
                self.weiter.writerows(app_list)
                self.lock.release()
            except Exception as e:
                print(e)

    # 获取1个类别的应用总页数
    def get_total(self, id):
        url = self.url.format(0, id)
        html = json.loads(self.get_html(url))
        count = html["count"]
        if count % 30 == 0:
            total = count // 30
        else:
            total = count // 30 + 1
        return total

    # 入口函数
    def run(self):
        # 1.先让URL入队列
        self.get_all_id()
        # 2.多线程,开始执行
        t_list = []
        for i in range(1):
            t = Process(target=self.parse_html)
            t_list.append(t)
            t.start()
        for j in t_list:
            j.join()
        print("数量:", self.i)
        self.f.close()


if __name__ == '__main__':
    start_time = time.time()
    spider = XiaomiSpider()
    spider.run()
    end_time = time.time()
    print("执行时间:%.2f" % (end_time - start_time))
