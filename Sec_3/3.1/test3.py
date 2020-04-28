import urllib.request
import urllib.parse


# 传递一个字典，通过urllib.parse.urlencode将其转化为字符串，并指定编码格式，再转码成字节流数据
data = bytes(urllib.parse.urlencode({'word': 'hello'}), encoding='utf-8')
# httpbin.org提供HTTP请求测试，测试POST请求，并传递了data参数
response = urllib.request.urlopen('http://httpbin.org/post', data=data)
print(response.read().decode('utf-8'))