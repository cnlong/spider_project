from urllib.parse import urlsplit

res = urlsplit('http://www.baidu.com/index.html;user?id=5#comment')
print(res)