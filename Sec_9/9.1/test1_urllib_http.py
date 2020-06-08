from urllib.error import URLError
from urllib.request import ProxyHandler, build_opener

# 设置代理地址
# 如代理地址需要认证，传入用户名密码即可
# proxy = 'username:password@223.247.94.72:4216'
proxy = '113.101.151.171:4216'
# 设置代理处理对象，字典类型，键名为协议类型，键值为代理，访问相应协议，则调用对应的代理
proxy_handler = ProxyHandler({
    'http': 'http://' + proxy,
    'https': 'https://' + proxy
})
# 创建Opener对象，调用设置好的代理，并通过其open方法访问网页
opener = build_opener(proxy_handler)
try:
    response = opener.open('http://httpbin.org/get')
    print(response.read().decode('utf-8'))
except URLError as e:
    print(e.reason)