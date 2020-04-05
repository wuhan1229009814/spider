import csv

with open("fengyun.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["德玛", "暴风巨刃"])

hero_list = [
    ("步惊云", "绝世好剑"),
    ("雄霸", "三分归元气")
]
with open("fengyun.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(hero_list)








