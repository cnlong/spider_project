# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request, Spider


class WeibocnSpider(scrapy.Spider):
    name = 'weibocn'
    allowed_domains = ['m.weibo.cn']
    # 不定义start_urls，通过start_request生成
    # start_urls = ['http://m.weibo.cn/']
    # 定义几个微博的Ajax的URL
    user_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&luicode=10000011&containerid=100505{uid}'
    follow_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{uid}&page={page}'
    fan_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{uid}&since_id={id}'
    weibo_url = 'https://m.weibo.cn/api/container/getIndex?containerid=230413{uid}_-_WEIBO_SECOND_PROFILE_WEIBO&page_type=03&page={page}'
    # 起始微博用户的ID
    start_users = ['1798590865', '1674166903']

    def start_requests(self):
        for uid in self.start_urls:
            yield Request(url=self.user_url.format(uid=uid), callback=self.parse_user)

    def parse_user(self, response):
        self.logger.debug(response)

    def parse(self, response):
        pass
