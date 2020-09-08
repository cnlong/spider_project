# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import re
import csv
import pymongo
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline


class TextPipeline(object):
    """对获取到的值进一步优化处理"""
    def process_item(self, item, spider):
        if item['area']:
            if len(re.findall('\((.*)\)', item['area'])) > 0:
                item['area'] = re.findall('\((.*)\)', item['area'])[0]
            else:
                item['area'] = '--'
        if item['time']:
            if len(re.findall('\d+-\d+-\d+', item['time'])) > 0:
                item['time'] = re.findall('\d+-\d+-\d+', item['time'])[0]
            elif len(re.findall('\d+', item['time'])) > 0:
                item['time'] = re.findall('\d+', item['time'])[0]
        if item['star']:
            if len(re.findall('主演：(.*)', item['star'])) > 0:
                item['star'] = re.findall('主演：(.*)', item['star'])[0]
        return item


class WriteToFilePipeline(object):
    """存入csv文件"""
    def process_item(self, item, spider):
        # utf_8_sig格式导出不乱码
        with open('maoyantop100.csv', 'a', encoding='utf_8_sig', newline='') as f:
            fieldnames = ['index', 'thumb', 'name', 'star', 'area', 'time', 'score']
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writerow(dict(item))
        return item


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(mongo_uri=crawler.settings.get('MONGO_URI'),
                   mongo_db=crawler.settings.get('MONGO_DB'))

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        self.db[item.collection].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()


class ImagePipeline(ImagesPipeline):
    """保存图片"""
    def file_path(self, request, response=None, info=None):
        """获取保存的文件名"""
        url = request.url
        file_name = str(re.match('^.*movie/(.*\.jpg).*$', url).group(1))
        return file_name

    def get_media_requests(self, item, info):
        yield Request(item['thumb'])


class Maoyantop100Pipeline(object):
    def process_item(self, item, spider):
        return item
