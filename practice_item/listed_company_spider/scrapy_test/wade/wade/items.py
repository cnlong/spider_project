# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WadeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = 'stock'
    serial_number = scrapy.Field()
    stock_code = scrapy.Field()
    stock_abbre = scrapy.Field()
    company_name = scrapy.Field()
    province = scrapy.Field()
    city = scrapy.Field()
    main_bussiness_income = scrapy.Field()
    net_profit = scrapy.Field()
    employees = scrapy.Field()
    listing_date = scrapy.Field()
    zhaogushu = scrapy.Field()
    financial_report = scrapy.Field()
    industry_classification = scrapy.Field()
    industry_type = scrapy.Field()
    main_business = scrapy.Field()


