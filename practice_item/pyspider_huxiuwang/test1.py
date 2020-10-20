import requests


data = {
    'platform': 'www',
    'recommend_time': '1603155300',  # 查询的时间戳
    # 'pagesize': '22'
}

url = 'https://article-api.huxiu.com/web/article/articleList'
response = requests.post(url, data=data)
# \u字符串转成中文的编码格式
print(response.text.encode('utf-8').decode('unicode_escape'))
# json直接返回json格式字符串，捕获的中文也不会乱码
print(response.json()['data']['dataList'])