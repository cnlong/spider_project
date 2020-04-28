import http.cookiejar
import urllib.request


# 定义一个保存cookie的文件名
filename = 'cookies.txt'
# 声明cookie对象，并传入文件名
cookie = http.cookiejar.MozillaCookieJar(filename)
# 构建一个处理cookie的handler
handler = urllib.request.HTTPCookieProcessor(cookie)
# 创建opener
opener = urllib.request.build_opener(handler)
# 发送请求，只有发送请求之后，此前创建的cookie对象中才会存入cookie值
res = opener.open('http://www.baidu.com')
cookie.save(ignore_discard=True, ignore_expires=True)