import requests

r = requests.get("http://www.jianshu.com")
print('Request failed') if not r.status_code == requests.codes.ok else print('Request Successfully')