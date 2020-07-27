# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import quote
from scrapy import Request,Spider
from scrapyseleniumtest.items import ProductItem


class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    allowed_domains = ['www.taobao.com']
    start_urls = ['http://www.taobao.com/']
    # 淘宝关键字搜索的url
    base_url = 'https://s.taobao.com/search?q='

    def parse(self, response):
        # products = response.css('.m-itemlist .items .item')
        # for product in products:
        #     item = ProductItem()
        #     item['price'] = product.css('.ctx-box .price strong::text').extract_first()
        #     item['title'] = product.css('a.J_ClickStat::text').extract_first()
        #     item['shop'] = product.css('.shop::text').extract_first()
        #     item['image'] = product.css('.pic img::attr(data-src)').extract_first()
        #     item['deal'] = product.css('.deal-cnt::text').extract_first()
        #     item['location'] = product.css('.location::text').extract_first()
        #     print(item)
        #     yield item
        # xpath的选取精准度比css选取更准确
        # 注意 div[@class="items"]和div[contains(@class="items")]区别
        products = response.xpath(
            '//div[@id="mainsrp-itemlist"]//div[@class="items"][1]//div[contains(@class, "item")]')
        for product in products:
            item = ProductItem()
            item['price'] = ''.join(product.xpath('.//div[contains(@class, "price")]//text()').extract()).strip()
            item['title'] = ''.join(product.xpath('.//div[contains(@class, "title")]//text()').extract()).strip()
            item['shop'] = ''.join(product.xpath('.//div[contains(@class, "shop")]//text()').extract()).strip()
            item['image'] = ''.join(
                product.xpath('.//div[@class="pic"]//img[contains(@class, "img")]/@data-src').extract()).strip()
            item['deal'] = product.xpath('.//div[contains(@class, "deal-cnt")]//text()').extract_first()
            item['location'] = product.xpath('.//div[contains(@class, "location")]//text()').extract_first()
            print(item)
            yield item

    def start_requests(self):
        """开启爬取，生成request，放入调度器"""
        # 读取配置文件中关键词的列表
        for keyword in self.settings.get('KEYWORDS'):
            # 循环页码
            for page in range(1, self.settings.get('MAX_PAGE') + 1):
                # urlencode将字典形式的参数序列为url编码后的字符串，用于构造参数
                # quote用于将单个字符串序列化为Url编码格式的字符串
                url = self.base_url + quote(keyword)
                # 返回请求
                # meta想请求传入分页页码参数，而不是向url地址中传入，后续获取Page页码，通过浏览器的页码框进行跳转
                # scrapy默认会过滤重复网页，发起Request添加dont_filter=True，则可以重复请求
                yield Request(url=url, callback=self.parse, meta={'page': page}, dont_filter=True)