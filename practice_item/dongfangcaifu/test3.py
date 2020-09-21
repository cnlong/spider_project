import requests
import pandas as pd
from pyquery import PyQuery as pq
import time

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
    }

response = requests.get('http://data.eastmoney.com/bbsj/202006/lrb.html', headers=headers)
html = response.text
print(html)
# requests直接请求网页，无法获取想要的数据，因为网页本身获取数据需要时间，而requests瞬时获取页面，但是此时页面并未获取到数据

