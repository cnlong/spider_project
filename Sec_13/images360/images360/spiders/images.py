# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider, Request
from urllib.parse import urlencode
import json
from images360.items import ImageItem


class ImagesSpider(scrapy.Spider):
    name = 'images'
    allowed_domains = ['image.so.com']
    start_urls = ['http://image.so.com/']

    def parse(self, response):
        # 将json内容转换成字典
        result = json.loads(response.text)
        # 获取text内容中list字段中的图片并遍历
        for image in result.get('list'):
            # 创建item对象
            item = ImageItem()
            # 保存数据
            item['id'] = image.get('id')
            item['url'] = image.get('qhimg_thumb')
            item['title'] = image.get('title')
            item['thumb'] = image.get('qhimg_url')
            print('item', item)
            yield item

    def start_requests(self):
        # url参数
        data = {'ch': 'photograph', 'listtype': 'new'}
        # 基础url
        base_url = 'https://image.so.com/zjl?'
        # 遍历页数
        for page in range(1, self.settings.get('MAX_PAGE') + 1):
            # 计算sn号
            data['sn'] = page * 30
            # url参数编码转换
            params = urlencode(data)
            url = base_url + params
            # 发起请求
            yield Request(url, self.parse)
