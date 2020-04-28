import urllib.request


response = urllib.request.urlopen('https://www.python.org')
print(response.status)
# 输出响应头的信息，列表形式显示
print(response.getheaders())
# 获取响应头中Server的值
print(response.getheader('Server'))
print(dir(response))