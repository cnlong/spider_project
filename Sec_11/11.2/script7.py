import json
import pymongo
from mitmproxy import ctx


client = pymongo.MongoClient('192.168.6.160')
db = client['igetget']
collection = db['books']


def response(flow):
    url = "https://entree-ali.igetget.com/cornflower/v1/operation/rank/get"
    if flow.request.url.startswith(url):
        text = flow.response.text
        data = json.loads(text)
        books = data.get('c').get('list')[0].get('list')
        for book in books:
            data = {
                'title': book.get('title'),
                'cover': book.get('index_img'),
                'summary': book.get('intro'),
                'price': book.get('cost_intro').get('price')
            }
            ctx.log.info(str(data))