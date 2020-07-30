# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapyyuniversal.items import NewsItem


class ChinaSpider(CrawlSpider):
    name = 'china'
    allowed_domains = ['tech.china.com']
    start_urls = ['https://tech.china.com/articles']

    rules = (
        # LinkExtractor,只提取每条新闻的链接地址，并通过正则匹配只是以article开头的链接
        # 提取出来的链接会自动生成Request，放入到调度器中
        # allow 正则匹配，restrict_xpath通过xpath选定一块区域，然后spider会提取该区域的所有超链接生成REquest
        # 着重注意xpath规则的编写，注意具有多个class属性标签块的获取规则
        Rule(LinkExtractor(allow=r'article\/.*\.html', restrict_xpaths='//div[@id="rank-defList"]//h3[@class="tit"]'),
             callback='parse_item', follow=True),
        # Rule(LinkExtractor(allow=r'article\/.*\.html', restrict_css='#rank-defList .tit'), callback='parse_item', follow=True),
        # 提取下一页的请求，无需回调函数，follow默认为true
        # 注意xpath提取的时候，提取包含文本内容的格式
        Rule(LinkExtractor(restrict_xpaths='//div[@class="pages"]//a[contains(., "下一页")]')),
    )

    def parse_item(self, response):
        item = NewsItem()
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        item['title'] = response.xpath('//h1[@id="chan_newsTitle"]//text()').extract_first()
        yield item
