from urllib import request, error

try:
    res = request.urlopen('https://cuiqingcai.com/index.html')
    print(res.read().decode('utf-8'))
except error.HTTPError as e:
    print(e.reason, e.code, e.headers, sep='\n')
except error.URLError as e:
    print(e.reason)