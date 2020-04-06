"""
向测试网站发请求,并获取响应内容
"""
import requests

url = "http://www.baidu.com/"
headers = {"User-Agent": "Wherever you go"}

res = requests.get(url=url, headers=headers)
# 1.获取响应对象内容 - 字符串
res.encoding = "utf-8"
html = res.text
print(html)

# 2.获取响应对象内容 - 字节串
html = res.content
# 3.获取HTTP响应码
code = res.status_code
# 4.返回实际数据的URL地址
data_url = res.url


# html = requests.get(url=url, headers=headers).text




