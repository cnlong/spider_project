# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import pymysql
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class Images360Pipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    """存储数据到MongoDB中"""
    def __init__(self, mongo_url, mongo_db):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(mongo_url=crawler.settings.get('MONGO_URL'),
                   mongo_db=crawler.settings.get('MONGO_DB'))

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        self.db[item.collection].insert(dict(item))
        # 只对数据进行存储，不做其他内容改变，因为其还要被其他的Pipeline处理
        return item

    def close_spider(self, spider):
        self.client.close()


class MysqlPipeline(object):
    """存储数据到MySQL"""
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(host=crawler.settings.get('MYSQL_HOST'),
                   database=crawler.settings.get('MYSQL_DATABASE'),
                   user=crawler.settings.get('MYSQL_USER'),
                   password=crawler.settings.get('MYSQL_PASSWORD'),
                   port=crawler.settings.get('MYSQL_PORT'))

    def open_spider(self, spider):
        # 注意，连接MySQL的时候，端口需要的是数字，而不是字符串，否则报错
        self.db = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database, charset='utf8', port=self.port)
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        data = dict(item)
        # 构建sql语句
        keys = ",".join(data.keys())
        values = ",".join(['%s'] * len(data))
        sql = 'insert into %s (%s) values (%s)' % (item.table, keys, values)
        # 将item的值转换成元组，插入到sql语句中
        self.cursor.execute(sql, tuple(data.values()))
        self.db.commit()
        # 只对数据进行存储，不做其他内容改变，因为其还要被其他的Pipeline处理
        return item


class ImagePipeline(ImagesPipeline):
    """自定义Pipeline，重写父类的部分方法"""
    def file_path(self, request, response=None, info=None):
        """
        "重写定义文件的名称
        :param request: get_media_requests方法中新生成的request对象
        :param response: 默认为None
        :param info: 默认为None
        :return:
        """
        # 截取新生成的request对象URL地址中图片的名称，作为图片保存的名称
        url = request.url
        file_name = url.split('/')[-1]
        return file_name

    def item_completed(self, results, item, info):
        """
        分析item下载的结果，下载失败，抛出DropItem异常，那么其他的Pipeline就会忽略该Item，也就是MongoDB和MySQL的Pipeline
        不将其保存至数据库中
        :param results: 该item的url下载结果
        :param item: 该item对象
        :param info:
        :return:
        """
        # result下载结果是一个列表，包含着下载的成功或失败所有结果信息
        # 如果下载成功，列表中会包含ok和x的元组，遍历该列表，获取成功的信息，image_path不为空
        # 如果下载失败，那么就获取不到成功的信息，那么image_path为空
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('Image Download Fialed')
        return item

    def get_media_requests(self, item, info):
        """
        获取item的url字段，生成Request请求对象
        :param item:  处理的item对象
        :param info:
        :return:
        """
        # 获取item对象中的url地址，并生成一个新的Request对象，放入调度队列中，等待调度
        yield Request(item['url'])