#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2020-10-20 03:51:35
# Project: huxiu

from pyspider.libs.base_handler import *
import pymongo
import time
import json
import pandas as pd

client = pymongo.MongoClient('192.168.6.160')
db = client.huxiu
mongo_collection = db.huxiu_pyspider


class Handler(BaseHandler):
    crawl_config = {
        "headers": {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
        }
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://article-api.huxiu.com/web/article/articleList', method='POST', data={'platform': 'www'},
                   callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        content = response.json
        datalist = content['data']['dataList']
        last_dateline = content['data']['last_dateline']
        articles = [{
            'title': item['title'],
            'url': item['share_url'],
            'author': item['user_info']['username'],
            'write_time': item['formatDate'],
            'comment': item['count_info']['commentnum'],
            'favourites': item['count_info']['favtimes'],
            'shares': item['count_info']['sharetimes']
        } for item in datalist]
        if articles:
            self.save_to_mongo(articles)
        self.crawl('https://article-api.huxiu.com/web/article/articleList', method='POST',
                   data={'platform': 'www', 'recommend_time': last_dateline}, callback=self.index_page)

    def save_to_mongo(self, result):
        df = pd.DataFrame(result)
        print(db)
        content = json.loads(df.T.to_json()).values()
        print(content)
        if mongo_collection.insert_many(content):
            print("存储成功！")

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }
