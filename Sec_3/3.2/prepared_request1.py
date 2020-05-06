from requests import Session, Request

url = "http://httpbin.org/post"
data = {
    'name': 'germey'
}
headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
}
# 构建session对象
s = Session()
# 构建Request对象
req = Request('POST', url, data=data, headers=headers)
# 构建prepared request对象
prepped = s.prepare_request(req)
# 通过session发送请求
r = s.send(prepped)
print(r.text)
