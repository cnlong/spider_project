from lxml.html import etree

text = """
<li class="li li-first" name="item"><a href="link6.html">sixth item</a></li>
"""
html = etree.HTML(text)
result = html.xpath('//li[contains(@class, "li") and @name="item"]/a/text()')
print(result)