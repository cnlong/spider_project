from scrapy import Selector

body = '<html><head><title>Hello World</title></head><body></body></html>'
# 定义selector对象
selector = Selector(text=body)
# 提取，注意提取对象方法
title = selector.xpath('//title/text()').extract_first()
print(title)