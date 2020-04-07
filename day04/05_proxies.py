import requests

url = 'http://httpbin.org/get'
headers = {"User-Agent": "xxxxxxxxxx"}
proxies = {
    "http": "http://117.88.4.41:3000",
    "https": "https://117.88.4.41:3000"
}
html = requests.get(url=url, proxies=proxies, headers=headers).text
print(html)
