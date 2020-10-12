"""
IT桔子网站模拟登录
"""
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
}

account = input('用户名：')
password = input('密码：')
data = {
    'account': account,
    'password': password
}
url = 'https://www.itjuzi.com/api/authorizations'
# 通过Session共享，先登录后访问其他页面
session = requests.Session()
session.post(url, headers=headers, data=data)
response = session.get('https://www.itjuzi.com/', headers=headers)
print(response.status_code)
print(response.text)