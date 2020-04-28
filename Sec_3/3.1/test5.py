import urllib.request


# 通过Request类构造请求，可以灵活的传入参数
request = urllib.request.Request('https://python.org')
# 通过urlopen来发送请求
response = urllib.request.urlopen(request)
print(response.read().decode('utf-8'))