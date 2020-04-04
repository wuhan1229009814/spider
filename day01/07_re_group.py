import re

s = 'A B C D'
p1 = re.compile('\w+\s+\w+')
print(p1.findall(s))
# 分析结果是什么？？？
# ['A B','C D']
p2 = re.compile('(\w+)\s+\w+')
print(p2.findall(s))
# 第1步: ['A B','C D']
# 第2步: ['A','C']

p3 = re.compile('(\w+)\s+(\w+)')
print(p3.findall(s))
# 第1步: ['A B','C D']
# 第2步: [('A','B'),('C','D')]
