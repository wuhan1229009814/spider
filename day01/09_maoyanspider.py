"""
爬取猫眼电影信息
"""
from urllib import request
import re
import pymysql

# 1.定义常用变量
url = "https://maoyan.com/board/4"
headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"}
db = pymysql.connect("localhost", "root", "123456", "mydb", cahrset="utf8")
cursor = db.cursor()

# 2.请求
req = request.Request(url=url, headers=headers)
resp = request.urlopen(req)
html = resp.read().decode()

# 3.解析提取数据
regex = '<div class="movie-item-info">.*?title="(.*?)".*?<p class="star">(.*?)</p>.*?<p class="releasetime">(.*?)</p>'
pattern = re.compile(regex, re.S)
film_list = pattern.findall(html)
item = {}
for film in film_list:
    item["name"] = film[0].strip()
    item["star"] = film[1].strip()
    item["time"] = film[2].strip()
    print(item)
    # 4.数据入库
    ins = "insert into mytab values(%s,%s,%s)"
    cursor.execute(ins, [item['name'], item["star"], item["time"]])
    db.commit()





