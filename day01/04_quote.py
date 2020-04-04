"""
向百度输入搜索关键字,保存响应内容到本地文件: xxx.html
"""
from urllib import request, parse

# 1.拼接URL地址
url = "http://www.baidu.com/s?wd={}"
word = input("请输入搜索关键字:")
params = parse.quote(word)
full_url = url.format(params)

# 2.发请求获取响应内容
headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0)"}
req = request.Request(url=full_url, headers=headers)
resp = request.urlopen(req)
html = resp.read().decode()

# 3.保存到本地文件
filename = "{}.html".format(word)
with open(filename, "w") as f:
    f.write(html)
