from urllib.parse import urlunsplit

res = ['http', 'www.baidu.com', 'index.html', 'a=6', 'comment']
print(urlunsplit(res))