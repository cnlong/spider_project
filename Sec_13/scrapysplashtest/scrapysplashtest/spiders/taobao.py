# -*- coding: utf-8 -*-
import scrapy
import json
from urllib.parse import quote, urlencode
from scrapysplashtest.items import ProductItem
from scrapy_splash import SplashRequest


# splash的LUA脚本
script = '''
function main(splash, args)
	splash.images_enabled = false
    assert(splash:go(args.url))
    splash:init_cookies(args.cookies)
    assert(splash:go(args.url))
    assert(splash:wait(args.wait))
    return splash:html()
end
'''


class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    allowed_domains = ['www.taobao.com']
    start_urls = ['http://www.taobao.com/']
    base_url = 'https://s.taobao.com/search?q='

    def parse(self, response):
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

    def get_cookies(self, file):
        with open(file, "r") as f:
            # 读取之前保存的cookies，将其转换成由单个cookie字典组成的列表
            cookies = json.load(f)
        # 遍历cookies列表，排除cookie中的expory参数，因为splash中 没有这个参数
        # 若保存这个参数，需要另外步骤处理
        # 若直接去除这个参数，也对结果没有影响
        for cookie in cookies:
            if "expiry" in cookie.keys():
                cookie.pop("expiry")
        return cookies

    # 对每一页的url构建一个splash请求
    def start_requests(self):
        # 获取splash地址
        splash_url = self.settings.get('SPLASH_URL')
        cookies = self.get_cookies(self.settings.get('JSON_PATH'))
        for keyword in self.settings.get('KEYWORDS'):
            for page in range(1, self.settings.get('MAX_PAGE') + 1):
                # 根据page页码进行url构建
                # 这样对每一页的请求构建一个url，然后对每一个url生成一个splashrequest，将cookies加入
                # 也可以通过splash的evaljs()方法调用js代码，实现页码的填充和翻页点击，返回下一页的请求
                if page == 1:
                    url = self.base_url + quote(keyword)
                else:
                    url = self.base_url + quote(keyword) + '&' + urlencode({'s': 44*(page-1)})
                yield SplashRequest(url=url, callback=self.parse, endpoint='execute',
                                    splash_url=splash_url,
                                    args={'lua_source': script, 'wait': 5, 'cookies': cookies})
