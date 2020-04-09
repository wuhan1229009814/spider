from threading import Thread


# 线程的事件函数
def parse_html():
    print("生活在这个陌生的城市里")


t_list = []
for i in range(5):
    t = Thread(target=parse_html)
    t.start()
    t_list.append(t)

for j in t_list:
    j.join()
