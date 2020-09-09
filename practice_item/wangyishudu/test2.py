import requests
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
}

url = 'http://data.163.com/20/0907/16/FLUEM8EP00019GOE.html'
response = requests.get(url, headers=headers)
if response.status_code == 200:
    html = response.text

# soup = BeautifulSoup(html, 'lxml')
# items = soup.select('section > p > img')
# for item in items:
#     print({'url': item['src']})
data = pq(html)('section > p > img')
print(list(data.items())[0].attr('src'))
for item in data.items():
    print({'url': item.attr('src')})

