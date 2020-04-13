"""
爬取京东商品详细信息
"""
from selenium import webdriver
import time


class JdSpider:
    def __init__(self):
        self.url = 'https://www.jd.com/'
        self.browser = webdriver.Chrome()
        self.browser.get(url=self.url)

    # 找到搜索框和搜索按钮进行操作
    def get_html(self):
        self.browser.find_element_by_xpath('//*[@id="key"]').send_keys('爬虫书')
        self.browser.find_element_by_xpath('//*[@id="search"]/div/div[2]/button').click()
        # 给页面元素加载预留时间
        time.sleep(1)

    # 功能:提取1页商品信息
    def get_one_page(self):
        # 执行js脚本,把进度条拉到最底部,并预留加载时间
        self.browser.execute_script(
            "window.scrollTo(0,document.body.scrollHeight)"
        )
        time.sleep(2)
        li_list = self.browser.find_elements_by_xpath('//*[@id="J_goodsList"]/ul/li')
        item = {}
        for li in li_list:
            goods_list = li.text.split("\n")
            if goods_list[0].startswith("￥"):
                item["price"] = goods_list[0]
                item["name"] = goods_list[1]
                item["commit"] = goods_list[2]
                item["shop"] = goods_list[3]
            else:
                item["price"] = goods_list[1]
                item["name"] = goods_list[2]
                item["commit"] = goods_list[3]
                item["shop"] = goods_list[4]
            print(item)

    # 入口函数
    def run(self):
        self.get_html()
        while True:
            self.get_one_page()
            if self.browser.page_source.find("pn-next disabled") == -1:
                self.browser.find_element_by_xpath('//*[@id="J_bottomPage"]/span[1]/a[9]').click()
                time.sleep(1)
            else:
                self.browser.quit()
                break


if __name__ == '__main__':
    spider = JdSpider()
    spider.run()


