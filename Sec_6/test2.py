"""
新版本中通过since_id获取响应，并提取响应内容。
"""
from urllib.parse import urlencode
import requests
from pyquery import PyQuery as pq
from pymongo import MongoClient
import json


def save_to_mongo(result):
    """mongodb存储数据"""
    client = MongoClient(host='192.168.6.160', port=27017)
    # 指定微博使用的库
    db = client['weibo1']
    # 指定库中的集合
    collection = db['weibo1']
    # 插入数据
    if collection.insert(result):
        print('Saved to Mongo Successfully!')


def parse_page(json):
    """
    解析返回的JSON内容
    :param json:
    :return:
    """
    if json:
        items = json.get('data').get('cards')
        for item in items:
            # 获取mbolg字段的信息
            item = item.get('mblog')
            weibo = {}
            weibo['id'] = item.get('id')
            # 通过pyquery解析正文中的HTML文档
            weibo['text'] = pq(item.get('text')).text()
            weibo['attitudes'] = item.get('attitudes_count')
            weibo['comments'] = item.get('comments_count')
            weibo['reposts'] = item.get('reposts_count')
            yield weibo


# 定义基本的url地址
base_url = 'https://m.weibo.cn/api/container/getIndex?'
# 定义头部信息
headers = {
    'Host': 'm.weibo.cn',
    'Referer': 'https://m.weibo.cn/u/2830678474',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}


def get_page():
    """先获取第一页显示的微博列表内容"""
    params = {
        'type': 'uid',
        'value': '2830678474',
        'containerid': '1076032830678474',
    }
    url = base_url + urlencode(params)
    response_list = list()
    # 循环获取URL及其响应数据
    while True:
            response = requests.get(url, headers=headers)
            print(response.status_code)
            try:
                # 获取第一个url返回响应中的since_id
                since_id = response.json().get('data').get('cardlistInfo').get('since_id')
            except:
                # 获取不到代表没有下一个链接了，并终止循环退出
                print("no weibo")
                break
            params = {
                'type': 'uid',
                'value': '2830678474',
                'containerid': '1076032830678474',
                'since_id': since_id
            }
            url = base_url + urlencode(params)
            print(url)


if __name__ == '__main__':
    get_page()

