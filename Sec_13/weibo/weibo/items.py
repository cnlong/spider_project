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


class UserRelationItem(scrapy.Item):
    """保存和用户相关的数据"""
    collection = 'users'
    id = scrapy.Field()
    follows = scrapy.Field()
    fans = scrapy.Field()


class WeiBoItem(scrapy.Item):
    """保存微博的数据"""
    collection = 'weibos'
    id = scrapy.Field()
    attitudes_count = scrapy.Field()
    comments_count = scrapy.Field()
    reposts_count = scrapy.Field()
    picture = scrapy.Field()
    pictures = scrapy.Field()
    source = scrapy.Field()
    text = scrapy.Field()
    raw_text = scrapy.Field()
    user = scrapy.Field()
    thumbnail = scrapy.Field()
    created_at = scrapy.Field()
    crawled_at = scrapy.Field()