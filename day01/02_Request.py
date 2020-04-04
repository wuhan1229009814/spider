"""
向测试网站发请求,确认请求头
"""
from urllib import request

url = "http://httpbin.org/get"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0"}
# 1.创建请求对象 - Request()
req = request.Request(url=url, headers=headers)

# 2.获取响应对象 - urlopen()
resp = request.urlopen(req)

# 3.获取响应内容
html = resp.read().decode()

print(html)



