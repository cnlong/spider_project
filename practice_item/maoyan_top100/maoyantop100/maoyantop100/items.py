# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Maoyantop100Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = 'top100film'
    index = scrapy.Field()
    thumb = scrapy.Field()
    name = scrapy.Field()
    star = scrapy.Field()
    area = scrapy.Field()
    time = scrapy.Field()
    score = scrapy.Field()
