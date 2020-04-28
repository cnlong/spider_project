from urllib.parse import urlparse

res = urlparse('http://www.baidu.com/index.html;user?id=5#comment')
print(type(res), res, sep='\n')