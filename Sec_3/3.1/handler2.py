from urllib.request import ProxyHandler, build_opener
from urllib.error import URLError


# 假设在本地的9743端口上搭建了一个代理
# 构建一个代理处理器，传入一个字典，键名为协议类型，键值为代理链接，可添加多个代理
proxy_handler = ProxyHandler({
    'http': 'http://127.0.0.1:9473',
    'https': 'https://127.0.0.1:9473',
})

# 构建opener，传入代理处理器
opener = build_opener(proxy_handler)
# 发送请求
try:
    res = opener.open('https://www.baidu.com')
    print(res.read().decode('utf-8'))
except URLError as e:
    print(e.reason)