import requests
import os

url = "http://img2015.zdface.com/20180122/83e1ec680ec942849794a82a6faed440.jpeg"
headers = {"User-Agent": "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50"}

# 1.发请求
html = requests.get(url=url, headers=headers).content

# 保存到/home/tarena/images/
directory = "/home/tarena/images/"
if not os.path.exists(directory):
    os.makedirs(directory)

# 2.直接保存图片
filename = directory + url[-10:]
with open(filename, "wb") as f:
    f.write(html)
