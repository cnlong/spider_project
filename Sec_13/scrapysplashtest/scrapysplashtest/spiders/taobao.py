# -*- coding: utf-8 -*-
import scrapy


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

    def parse(self, response):
        pass
