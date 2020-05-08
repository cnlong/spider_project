from lxml.html import etree

html = etree.parse('test.html', etree.HTMLParser())
result = html.xpath('//li[contains(@class, "li")]/a/text()')
print(result)