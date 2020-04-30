import requests

r = requests.get("http://www.jianshu.com")
print(dir(r))
print(type(r.status_code), r.status_code)
print(type(r.headers), r.headers)
print(type(r.url), r.url)