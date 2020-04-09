"""
browser.page_source # HTML结构源码
browser.page_source.find('字符串')
"""
from selenium import webdriver

browser = webdriver.Firefox()
browser.get("http://www.baidu.com/")

# 找不到某个字符串返回-1
print(browser.page_source.find("su"))
browser.quit()
