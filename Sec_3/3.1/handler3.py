import http.cookiejar
import urllib.request


# 声明cookie对象
cookie = http.cookiejar.CookieJar()
# for item in cookie:
#     print(item.name+"="+item.value)
# 构建一个处理cookie的handler
handler = urllib.request.HTTPCookieProcessor(cookie)
# 创建opener
opener = urllib.request.build_opener(handler)
# 发送请求，只有发送请求之后，此前创建的cookie对象中才会存入cookie值
res = opener.open('http://www.baidu.com')
for item in cookie:
    print(item.name+"="+item.value)