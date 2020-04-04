import re


html = """
<div class="animal">
    <p class="name">
        <a title="Tiger"></a>
    </p>
    <p class="content">
        Two tigers two tigers run fast
    </p>
</div>

<div class="animal">
    <p class="name">
        <a title="Rabbit"></a>
    </p>

    <p class="content">
        Small white rabbit white and white
    </p>
</div>
"""
regex = '<div class="animal">.*?<a title="(.*?)">.*?<p class="content">(.*?)</p>'
p = re.compile(regex, re.S)
p_list = p.findall(html)
print(p_list)

for p in p_list:
    print("动物名称:", p[0].strip())
    print("动物描述:", p[1].strip())
    print("*" * 50)
