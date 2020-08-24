# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import re, time
import pymongo
from weibo.items import UserItem, WeiboItem, UserRelationItem


class TimePipeline(object):
    """
    默认给所有的item增加一个crawled_at字段，保存爬取时间
    需要添加爬取时间的item只有UserItem和WeiboItme
    """
    def process_item(self, item, spider):
        # 判断其是不是需要爬取时间的Item
        if isinstance(item, UserItem) or isinstance(item. WeiboItem):
            # 获取当前时间
            now = time.strftime('%Y-%m-%d %H:%M', time.localtime())
            item['crawled_at'] = now
        return item


class WeiboPipeline(object):
    """对于微博创建时间的转换"""
    def parse_time(self, date):
        """
        对时间进行转换的函数
        :param date: 爬取到的实际
        :return: 转换后的时间
        """
        if re.match('刚刚', date):
            # time.time()将当前时间转换为时间戳
            # time.localtime()将时间戳转换为本地时间，参数为空则以当前时间输入
            # time.strftime()将时间元组转换为字符串格式
            date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
        if re.match('\d+分钟前', date):
            # 提取时间数字
            minute = re.match('(\d+)', date).group(1)
            # 时间戳的单位是秒数
            date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time() - float(minute) * 60))
        if re.match('\d+小时前', date):
            # 提取时间数字
            hour = re.match('(\d+)', date).group(1)
            # 时间戳的单位是秒数
            date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time() - float(hour) * 60 * 60))
        if re.match('昨天.*', date):
            # 提取时间刻度，例如昨天 13:14
            date = re.match('昨天(.*)', date).group(1).strip()
            # 获取获取24小时之前的时间戳，转换为字符串，加上昨天的时间刻度即可
            date = time.strftime('%Y-%m-%d', time.localtime(time.time() - 24 * 60 * 60)) + ' ' + date
        # 匹配只有月日的微博时间
        if re.match('\d{2}-\d{2}' ,date):
            # 获取年，组合日月和时间
            date = time.strftime('%Y', time.localtime()) + date + '00:00'
        return date

    def process_item(self, item, spider):
        """对微博时间进行处理"""
        if isinstance(item, WeiboItem):
            # 获取捕获到的创建时间
            if item.get('created_at'):
                # 清除时间两边的空白
                item['created_at'] = item['created_at'].strip()
                # 调用函数处理时间
                item['created_at'] = self.parse_time(item.get('created_at'))
            # 捕获到具有多张图片的微博时候，其pictures字段保存的是多张图片的信息列表，
            # 列表中字典形式保存每个图片的信息，包括url，需要提取出url，重新保存该字段
            if item.get('pictures'):
                item['pictures'] = [pic.get('url') for pic in item.get('pictures')]
            return item


class MongoPipeline(object):
    """将数据保存至MongoDB"""
    # 初始化MongoDB的连接信息
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    # 从配置信息中获取MongoDB的配置
    @classmethod
    def from_crawler(cls, crawler):
        # 返回一个实例对象
        return cls(mongo_uri=crawler.settings.get('MONGO_URI'),
                   mongo_db=crawler.settings.get('MONGO_DATABASE'))

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        # 构建索引，大规模数据检索方便
        # 按id升序构建索引
        self.db[UserItem.collection].create_index([('id', pymongo.ASCENDING)])
        self.db[WeiboItem.collection].create_index([('id', pymongo.ASCENDING)])

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # 对数据进行处理保存
        if isinstance(item, UserItem) or isinstance(item, WeiboItem):
            # 按照id对数据进行更新，先查询，如果查询到数据则进行更新，如果查询不到，则插入新数据
            # 第一个参数为查询条件，第二个参数是爬取的item，数据存在即更新，数据不存在即插入，获得去重的数据
            # 如果不设置$set，则会进行item替换，会删除已存在的数据
            self.db[item.collection].update({'id': item.get('id')}, {'$set': item}, True)
        if isinstance(item, UserRelationItem):
            # UserRelationItem在保存数据的时候，存在两种情况，一种是只有粉丝数，一种是只有关注数
            # 在向MongoDB进行存储的时候进行合并
            self.db[item.collection].update(
                {'id', item.get('id')},
                # 增加字段数据，字段没有数据则添加，有则不添加
                # 例如，第一次获取到item = {'id': 001, 'follows': 100, 'fans': ''}
                # 第一次更新id=001的数据时候，直接插入
                # 第二次获取item = {'id': 001, 'follows': '', 'fans': 100}
                # 第二次进行更新id=001的粉丝数量时，只更新fans字段
                # 注意使用$addToSet的方式添加，增加一个值到某个字段中，只有当这个值不在字段的值内才增加
                # 向列表类型的字段插入数据同时去重，使用$each遍历要插入列表的数据，如果已经存在即更新，如果不存在即插入
                {'$addToSet':
                     {
                         'follows': {'$each', item['follows']},
                         'fans': {'$each', item['fans']},
                     }
                }, True
            )
        return item