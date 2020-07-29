# -*- coding: utf-8 -*-
# 通过splash执行evajs()方法在页面上进行翻页，无需分析请求URL的规律，
# 打开初始URL，然后根据传入的Page页码，进行对应页面跳转即可
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
    js = string.format("document.querySelector('#mainsrp-pager div.form > input').value=%d;document.querySelector('#mainsrp-pager div.form > span.btn.J_Submit').click()", args.page)
    splash:evaljs(js)
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
                # 向splash中传入翻页页码，然后调用js执行翻页操作
                url = self.base_url + quote(keyword)
                yield SplashRequest(url=url, callback=self.parse, endpoint='execute',
                                    splash_url=splash_url,
                                    args={'lua_source': script, 'wait': 5, 'cookies': cookies, 'page': page})
