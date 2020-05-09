from lxml.html import etree

# 读取文本文件进行解析
# 传入解析的文件，和解析方法
html = etree.parse('test.html', etree.HTMLParser())
result = etree.tostring(html)
print(result.decode('utf-8'))