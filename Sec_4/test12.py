from lxml.html import etree

html = etree.parse('test.html', etree.HTMLParser())
result = html.xpath('//li[1]/a/text()')
print(result)
result = html.xpath('//li[last()]/a/text()')
print(result)
result = html.xpath('//li[position()<3]/a/text()')
print(result)
result = html.xpath('//li[last()-2]/a/text()')
print(result)

# 获取第一个Li元素的祖先所有元素
result = html.xpath('//li[1]/ancestor::*')
print(result)
# 获取第一个Li元素的祖先的div元素
result = html.xpath('//li[1]/ancestor::div')
print(result)
# 获取第一个Li元素的属性值
result = html.xpath('//li[1]/attribute::*')
print(result)
# 获取第一个Li元素的子节点中href属性为"link1.html"的元素
result = html.xpath('//li[1]/child::a[@href="link1.html"]')
print(result)
# 获取第一个Li元素的所有子孙节点中span节点
result = html.xpath('//li[1]/descendant::span')
print(result)
# 获取第一个Li元素所在节点后的所有节点（不分级别）
result = html.xpath('//li[1]/following::*')
print(result)
# 获取第一个Li元素所在节点后的所有同级节点
result = html.xpath('//li[1]/following-sibling::*')
print(result)