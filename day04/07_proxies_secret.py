"""
开放代理使用
提取20个私密代理IP,一次测试每个IP是否可用,把可用的保存
"""
import requests


class ProxyPool:
    def __init__(self):
        self.url = ''
        self.headers = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)"}

    # 提取代理IP + 测试代理IP
    def parse_html(self):
        html = requests.get(url=self.url, headers=self.headers).text
        proxy_list = html.split("\r\n")
        for proxy in proxy_list:
            # 函数:测试1个代理是否可用
            self.test_proxy(proxy)

    # 函数:测试代理
    def test_proxy(self, proxy):
        # 私密代理使用必须加用户名和密码
        proxies = {
            "http": "http://{}".format(proxy),
            "https": "https://{}".format(proxy)
        }
        test_url = 'http://httpbin.org/get'
        auth = ("", "")
        try:
            resp = requests.get(url=test_url, proxies=proxies, auth=auth ,headers=self.headers, timeout=3)
            if resp.status_code == 200:
                # print('%s可用' % proxy)
                print('\033[031m%s可用\033[0m不可用' % proxy)
        except Exception as e:
            print("%s不可用" % proxy)

    def run(self):
        self.parse_html()


if __name__ == '__main__':
    spider = ProxyPool()
    spider.run()
