"""
selenium移动鼠标
"""
from selenium import webdriver
# 导入鼠标事件类
from selenium.webdriver import ActionChains
import time

# 1.打开浏览器输入百度
browser = webdriver.Chrome()
browser.get(url="http://www.baidu.com/")

# 2.移动鼠标到 设置 节点
set_node = browser.find_element_by_xpath('//*[@id="u1"]/a[8]')
ActionChains(browser).move_to_element(set_node).perform()
time.sleep(0.5)

# 3.点击高级搜索节点
browser.find_element_by_link_text("高级搜索").click()
