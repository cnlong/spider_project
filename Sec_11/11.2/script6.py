import json
from mitmproxy import ctx

def response(flow):
    url = "https://entree-ali.igetget.com/cornflower/v1/operation/rank/get"
    if flow.request.url.startswith(url):
        text = flow.response.text
        data = json.loads(text)
        # 注意返回的JSON字符串中的格式，找到电子书对应保存的列表
        books = data.get('c').get('list')[0].get('list')
        for book in books:
            print(book)