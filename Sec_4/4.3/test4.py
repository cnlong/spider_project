from pyquery import PyQuery as pq

html = """
<div class="wrap">
<div id="container">
<ul class="list">
<li class='item-0'>first item</li>
<li class='item-1'><a href="link2.html">second item</a></li>
<li class='item-0 active'><a href="link3.html"><span class="bold">third item</span></a></li>
<li class='item-1 active'><a href="link4.html">fourth item</a></li>
<li class='item-0'><a href="link5.html">fifth item</a></li>
</ul>
</div>
</div>
"""

doc = pq(html)
print(doc('#container .list li'))
print(type(doc('#container .list li')))

item = doc('.list')
print(type(item))
print(item)
print(type(item.find('li')))
print(item.find('li'))
print(type(item.children()))
print(item.children())
print(item.children('.active'))

container = item.parent()
print(container)

print("*"*50)
lis = doc('li').items()
print(type(lis))
for i in lis:
    print(i, type(i))

print("*"*50)
a = doc('.item-0.active a')
print(a.attr('href'))
print(a.attr.href)

print("*"*50)
a = doc('a')
print(a.attr('href'))

print("*"*50)
li = doc(".item-0.active")
print(li)
li.remove_class("active")
print(li)
li.add_class('active')
print(li)

print("*"*50)
li = doc(".item-0.active")
print(li)
li.attr('name', 'link')
print(li)
li.text('changed item')
print(li)
li.html('<e>hahah</e>')
print(li)

print("*"*50)
li = doc("li:first-child")
print(li)
li = doc("li:last-child")
print(li)
# 获取偶数节点
li = doc("li:nth-child(2n)")
print(li)
# 获取索引大于2的节点
li = doc("li:gt(2)")
print(li)
# 获取包含某一文本的节点
li = doc("li:contains(second)")
print(li)