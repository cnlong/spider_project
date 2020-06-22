import requests
from lxml.html import etree


headers = {
            'Referer': 'https://github.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
            'Host': 'github.com'
        }
login_url = 'https://github.com/login'

session = requests.session()

response = session.get(login_url, headers=headers)
selector = etree.HTML(response.text)
token = selector.xpath("//form/input[1]/@value")[0]
print(token)