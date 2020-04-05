"""
在aid1909db库里面新建集合aid1909set,并插入1条文档:{"name":"赵敏"}
"""
import pymongo

# 1.创建数据库连接对象
conn = pymongo.MongoClient("localhost", 27017)

# 2.创建库对象
db = conn["aid1909db"]

# 3.创建集合对象
myset = db["aid1909set"]

# 4.插入文档
myset.insert_one({"name": "赵敏"})

