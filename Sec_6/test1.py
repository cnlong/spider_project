"""
通过旧版本url中的page不断获取链接，并提取响应内容。
"""
from urllib.parse import urlencode
import requests
from pyquery import PyQuery as pq
from pymongo import MongoClient

# 定义基本的url地址
base_url = 'https://m.weibo.cn/api/container/getIndex?'

# 定义头部信息
headers = {
    'Host': 'm.weibo.cn',
    'Referer': 'https://m.weibo.cn/u/2830678474',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}

def get_page(page):
    """
    根据page获取响应
    :param page: 微博的页面
    :return:
    """
    # 定义url后面的参数字典
    params = {
        'type': 'uid',
        'value': '2830678474',
        'containerid': '1076032830678474',
        'page': page
    }

    # 将参数构成的字典传入urlencode()中，转换成key1=value1&key2=value2这样的字符串，和基础url合并成新的url
    url = base_url + urlencode(params)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    # 捕获异常
    except requests.ConnectionError as e:
        print('Error:', e.args)


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


def save_to_mongo(result):
    client = MongoClient(host='192.168.6.160', port=27017)
    # 指定微博使用的库
    db = client['weibo']
    # 指定库中的集合
    collection = db['weibo']
    # 插入数据
    if collection.insert(result):
        print('Saved to Mongo Successfully!')


if __name__ == '__main__':
    # 遍历10次获取10页的结果
    for page in range(1,11):
        json = get_page(page)
        results = parse_page(json)
        for result in results:
            print(result)
            save_to_mongo(result)
