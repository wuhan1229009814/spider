"""
登录QQ邮箱
url: https://mail.qq.com/
iframe: id login_frame
QQ: name u
密码: name p
登录: class btn
"""
from selenium import webdriver

# 1.打开网站
url = 'https://mail.qq.com/'
browser = webdriver.Chrome()
browser.get(url=url)

# 2.切换iframe子页面
frame_node = browser.find_element_by_id("login_frame")
browser.switch_to.frame(frame_node)

# 3.找节点开始登录
browser.find_element_by_name("u").send_keys("2621470058")
browser.find_element_by_name("p").send_keys("zhanshen001")
browser.find_element_by_class_name("btn").click()
