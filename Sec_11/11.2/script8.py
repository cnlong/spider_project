import json
from mitmproxy import ctx


def response(flow):
    url = "https://entree.igetget.com/cornflower/v1/operation/rank/get"
    if flow.request.url.startswith(url):
        text = flow.response.text
        data = json.loads(text)
        books = data.get('c').get('list')[0].get('list')
        for book in books:
            ctx.log.info(str(book))
        with open(r'E:\python_project\spider_project\Sec_11\11.2\books.txt', 'w') as f:
            f.write(str(books))