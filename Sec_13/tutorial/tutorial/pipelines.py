# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import pymongo


class TextPipeline(object):
    def __init__(self):
        self.limit = 50

    def process_item(self, item, spider):
        if item['text']:
            if len(item['text']) > self.limit:
                # 截取前50位，后面的用省略号代替
                item['text'] = item['text'][0:self.limit].rstrip() + '...'
            return item
        else:
            return DropItem('No Text')


class MongoPipeline(object):
    def __init__(self, mongo_url, mongo_db):
        # 定义连接mongodb的地址和数据库
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db

    # 定义类方法，通过传入的参数crawler，从全局配置中获取MongoDB的链接地址和数据库名称
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            # 通过crawler从本地的全局配置文件中，获取定义好的MONGO_URL和MONGO_DB变量的值
            mongo_url=crawler.settings.get('MONGO_URL'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    # 当Spider开启时候调用的方法，主要进行一些初始化操作，例如数据库的链接
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    # 定义处理Item对象的方法，这里将item插入数据库
    def process_item(self, item, spider):
        # 调用item对象的类的名称，作为数据库中表的名称
        name = item.__class__.__name__
        # 将item对象转为字典，存入到数据库中
        self.db[name].insert(dict(item))
        return item

    # 当spider关闭时候调用的方法，关闭上午开启的数据库连接
    def close_spider(self, spider):
        self.client.close()