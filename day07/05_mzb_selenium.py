import time

from selenium import webdriver


class MzbSpider:
    def __init__(self):
        self.url = 'http://www.mca.gov.cn/article/sj/xzqh/2019/'
        self.browser = webdriver.Chrome()
        self.browser.get(url=self.url)

    def parse_html(self):
        self.browser.find_element_by_xpath('//*[@id="list_content"]/div[2]/div/ul/table/tbody/tr[2]/td[2]/a').click()
        time.sleep(3)
        # 切换句柄
        all = self.browser.window_handles
        self.browser.switch_to.window(all[1])
        # 提取数据
        tr_list = self.browser.find_elements_by_xpath('//tr[@height="19"]')
        item = {}
        for tr in tr_list:
            # split()默认以空白作为切割
            info_list = tr.text.split()
            item["code"] = info_list[0]
            item["name"] = info_list[1]
            print(item)

    def run(self):
        self.parse_html()


if __name__ == '__main__':
    spider = MzbSpider()
    spider.run()







