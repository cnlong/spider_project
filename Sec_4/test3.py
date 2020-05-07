from lxml.html import etree
html = etree.parse('test.html', etree.HTMLParser())
# 匹配所有节点
result = html.xpath('//*')
print(result)