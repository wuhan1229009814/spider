"""
抓取猫眼电影top100
"""
from selenium import webdriver


url = 'https://maoyan.com/board/4'
# 1.创建浏览器对象,输入地址
options = webdriver.ChromeOptions()
options.add_argument("--headless")
browser = webdriver.Chrome(options=options)

# get()特点：　等页面所有元素加载完成后才会执行后续代码
browser.get(url=url)


def get_film_info():
    # 2.基准xpath,提取每个电影的节点对象列表[<dd>,<dd>,<dd>,...,<dd>]
    dd_list = browser.find_elements_by_xpath('//*[@id="app"]/div/div/div[1]/dl/dd')
    item = {}
    for dd in dd_list:
        li = dd.text.split("\n")
        item["rank"] = li[0]
        item["name"] = li[1]
        item["star"] = li[2]
        item["time"] = li[3]
        item["score"] = li[4]

        print(item)


while True:
    # 1.抓取第1页
    get_film_info()
    # 2.点击下一页(是否为最后一页)
    # 提示: browser.find_element_by_link_text("下一页") 找不到抛出异常
    try:
        browser.find_element_by_link_text("下一页").click()
    except Exception as e:
        print("抓取结束")
        browser.quit()
        break
