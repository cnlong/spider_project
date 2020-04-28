import http.cookiejar
import urllib.request


# 定义cookie对象
cookie = http.cookiejar.MozillaCookieJar()
# 读取本地的Cookies文件
cookie.load('cookies.txt', ignore_expires=True, ignore_discard=True)
# 构建一个cookie处理器
handler = urllib.request.HTTPCookieProcessor(cookie)
# 构建一个opener
opener = urllib.request.build_opener(handler)
# 发送请求
res = opener.open('http://www.baidu.com')
print(res.read().decode('utf-8'))