"""
打开firefox浏览器,输入百度,在搜索框输入 赵丽颖,点击 百度一下,停留在结果页面
"""
# 导入selenim的webdriver
from selenium import webdriver

# 1.打开浏览器 - 创建浏览器对象
browser = webdriver.Firefox()
# browser = webdriver.Chrome()
# browser = webdriver.PhantomJS()

# 2.输入http://www.baidu.com
browser.get("http://www.baidu.com")

# 发送文字 + 模拟点击
browser.find_element_by_xpath('//*[@id="kw"]').send_keys("赵丽颖")
browser.find_element_by_xpath('//*[@id="su"]').click()

# 获取截图
browser.save_screenshot("girl.png")

# 关闭浏览器
browser.quit()
