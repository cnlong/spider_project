import requests
from pyquery import PyQuery as pq

url = "http://www.zhihu.com/explore"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
}
html = requests.get(url, headers=headers).text
print(html)
doc = pq(html)
items = doc('.ExploreCollectionCard .ExploreHomePage-collectionCard')
print(items)
# for item in items:
#     questions = item.find('h2').text()
#     print(questions)
