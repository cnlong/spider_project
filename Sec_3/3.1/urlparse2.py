from urllib.parse import urlparse


res = urlparse('http://www.baidu.com/index.html;user?id=5#comment', allow_fragments=False)
print(res)
print(type(res))