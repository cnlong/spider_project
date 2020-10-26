import pymongo
import pandas as pd
import json
import requests


client = pymongo.MongoClient('192.168.6.160')
db = client.huxiu
collection = db.huxiu_new

url = 'https://article-api.huxiu.com/web/article/articleList'
data = {
    'platform': 'www',
    'pagesize': '22',
    # 'recommend_time': '1603155300'
}
response = requests.post(url, data=data)
time = 0
datas = list()
while True:
    if response.json()['success'] is True:
        recommend_time = response.json()['data']['last_dateline']
        for item in response.json()['data']['dataList']:
            datas.append(item)
    data = {
        'platform': 'www',
        'pagesize': '22',
        'recommend_time': recommend_time
    }
    response = requests.post(url, data=data)
    time += 1
    if time == 10:
        break
for item in datas:
    data = {
        'title': item['title'],
        'url': item['share_url'],
        'author': item['user_info']['username'],
        'write_time': item['formatDate'],
        'comment': item['count_info']['commentnum'],
        'favourites': item['count_info']['favtimes'],
        'shares': item['count_info']['sharetimes']
    }
    print(data)
