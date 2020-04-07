"""
使用独享代理访问已经被封掉的西刺代理
"""
import requests

url = 'https://www.xicidaili.com/'
headers = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)"}
proxies = {
    'http': 'http://309435365:szayclhp@49.7.96.227:16817',
    'https': 'https://309435365:szayclhp@49.7.96.227:16817'
}
html = requests.get(url=url, proxies=proxies, headers=headers).text
print(html)


