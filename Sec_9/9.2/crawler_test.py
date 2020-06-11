import requests
from pyquery import PyQuery as pq
import time

# page_count = 10
# start_url = 'https://www.kuaidaili.com/free/inha/{}/'
# urls = [start_url.format(page) for page in range(1, page_count+1)]
# for url in urls:
#     print("Crawing", url)
#     html = requests.get(url).content.decode('utf-8')
#     time.sleep(3)
#     doc = pq(html)
#     trs = doc('tbody tr').items()
#     for tr in trs:
#         ip = tr.find('td:nth-child(1)').text()
#         port = tr.find(('td:nth-child(2)')).text()
#         print(ip, port)

url = 'http://www.66ip.cn/1.html'
print("Crawing", url)
html = requests.get(url).content.decode('gbk')
doc = pq(html)
trs = doc('tr:gt(0)').items()
# print(trs)
for tr in trs:
    if tr.find('td:nth-child(1)').text() != 'ip':
        ip = tr.find('td:nth-child(1)').text()
        port = tr.find(('td:nth-child(2)')).text()
        print(ip, port)

