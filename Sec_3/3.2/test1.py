import requests

res = requests.get('https://www.baidu.com')
print(type(res))
print(res.status_code)
print(type(res.text))
print(res.text)
print(res.cookies)