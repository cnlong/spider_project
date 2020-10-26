"""数据爬取"""

import pymongo
import pandas as pd
import json
import requests
import time
import random


client = pymongo.MongoClient('192.168.6.160')
db = client.huxiu
collection = db.huxiu_new2

start_time = time.time()


def save_to_pymongo(result):
    # 将获取的数据转换成dataframe
    df = pd.DataFrame(result)
    # to_json将datafram转换成json，通过json转换成字典
    content = json.loads(df.T.to_json()).values()
    # print(content)
    if collection.insert_many(content):
        print('存储成功')


url = 'https://article-api.huxiu.com/web/article/articleList'
data = {
    'platform': 'www',
    'pagesize': '22',
    # 'recommend_time': '1603155300'
}
response = requests.post(url, data=data)
ns = 1
while True:
    datas = list()
    if response.json()['success'] is True:
        recommend_time = response.json()['data']['last_dateline']
        for item in response.json()['data']['dataList']:
            datas.append(item)
    datalist = list()
    for item in datas:
        dt = {
            'title': item['title'],
            'url': item['share_url'],
            'author': item['user_info']['username'],
            'write_time': item['formatDate'],
            'comment': item['count_info']['commentnum'],
            'favourites': item['count_info']['favtimes'],
            'shares': item['count_info']['sharetimes']
        }
        datalist.append(dt)
    print(datalist)
    print(recommend_time)
    if datalist == []:
        # print(recommend_time)
        break
    save_to_pymongo(datalist)
    data = {
        'platform': 'www',
        'pagesize': '22',
        'recommend_time': recommend_time
    }
    time.sleep(random.randint(0,3))
    response = requests.post(url, data=data)
    ns += 1
    print("第{}次开始爬取".format(ns))
    if ns == 500:
        break

print("耗时{}".format(time.time() - start_time))