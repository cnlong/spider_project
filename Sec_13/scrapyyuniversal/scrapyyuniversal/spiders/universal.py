# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapyyuniversal.utils import get_config
from scrapyyuniversal.rules import rules
from scrapyyuniversal.items import *
from scrapyyuniversal.loaders import *
from scrapyyuniversal import urls

class UniversalSpider(CrawlSpider):
    name = 'universal'

    def __init__(self, name, *args, **kwargs):
        # 根据传参读取配置文件
        config = get_config(name)
        self.config = config
        # 根据json中定义rules获取rules内容
        self.rules = rules.get(config.get('rules'))
        start_urls = config.get('start_urls')
        if start_urls:
            if start_urls.get('type') == 'static':
                self.start_urls = start_urls.get('value')
            if start_urls.get('type') == 'dynamic':
                # 注意self.start_urls必须是列表list
                # list(eval(urls.china)(*[5,10]))
                self.start_urls = list(eval('urls.' + start_urls.get('method'))(*start_urls.get('args', [])))
        self.allowed_domains = config.get('allowed_domains')
        # 调用父类__init__生成spider
        super(UniversalSpider, self).__init__(*args, **kwargs)

    def parse_item(self, response):
        item = self.config.get('item')
        if item:
            # 使用eval函数将字符串转换成表达式
            cls = eval(item.get('class'))()
            loader = eval(item.get('loader'))(cls, response=response)
            # 遍历获取属性
            for key, value in item.get('attrs').items():
                # 再遍历每个值（字典）
                for i in value:
                    # 根据不同的解析方法，制定不同的方法函数
                    if i.get('method') == 'xpath':
                        loader.add_xpath(key, *i.get('args'), **{'re': i.get('re')})
                    if i.get('method') == 'css':
                        loader.add_css(key, *i.get('args'), **{'re': i.get('re')})
                    if i.get('method') == 'value':
                        loader.add_value(key, *i.get('args'))
                    if i.get('method') == 'attr':
                        loader.add_value(key, getattr(response, *i.get('args')))
            yield loader.load_item()