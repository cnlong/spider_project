# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class UserItem(scrapy.Item):
    """用户详情"""
    collection = 'users'
    id = scrapy.Field()
    name = scrapy.Field()
    # 用户头像
    avatar = scrapy.Field()
    # 封面
    cover = scrapy.Field()
    gender = scrapy.Field()
    description = scrapy.Field()
    fans_count = scrapy.Field()
    follows_count = scrapy.Field()
    weibos_count = scrapy.Field()
    verified = scrapy.Field()
    verified_reason = scrapy.Field()
    verified_type = scrapy.Field()
    follows = scrapy.Field()
    fans = scrapy.Field()
    crawled_at = scrapy.Field()
