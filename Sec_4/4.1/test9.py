from lxml.html import etree

html = etree.parse('test.html', etree.HTMLParser())
result = html.xpath('//li/a/@href')
print(result)