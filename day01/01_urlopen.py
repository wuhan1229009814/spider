"""
向tmooc发起请求,并获取响应内容
"""
import urllib.request

# resp = urllib.request.urlopen("http://www.tmooc.cn/")
resp = urllib.request.urlopen("http://httpbin.org/get")
# 1.获取响应对象内容
html = resp.read().decode("utf-8")
print(html)
# 2.获取HTTP响应码
code = resp.getcode()
print(code)
# 3.获取返回实际数据的URL地址
url = resp.geturl()
print(url)









