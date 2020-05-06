import requests

r = requests.get('https://www.taobao.com', timeout=(5, 11))
print(r.status_code)