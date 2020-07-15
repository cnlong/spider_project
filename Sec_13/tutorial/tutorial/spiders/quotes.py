# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import QuoteItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        # 找出所有的quote元素标签块
        quotes = response.css('.quote')
        for quote in quotes:
            # 实例化Item对象
            item = QuoteItem()
            # 将数据保存至Item对象
            # 获取text节点正文
            # text = quote.css('.text::text').extract_first()
            item['text'] = quote.css('.text::text').extract_first()
            # 获取作者名称
            # author = quote.css('.author::text').extract_first()
            item['author'] = quote.css('.author::text').extract_first()
            # 获取标签tag列表
            # tags = quote.css('.tag::text').extract()
            item['tags'] = quote.css('.tag::text').extract()
            yield item
        # 获取下一页的链接地址
        next = response.css('.pager .next a::attr(href)').extract_first()
        # 将获取到相对URL构造成一个绝对的URL地址，比如获取到的是/page/2，通过
        # urljoin方法构造成http://quotes.toscrape.com/page/2
        url = response.urljoin(next)
        # 构造请求，并将响应传递给回调函数
        yield scrapy.Request(url=url, callback=self.parse)
