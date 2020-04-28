import socket
from urllib import request, error


try:
    res = request.urlopen('https://www.baidu.com', timeout=0.01)
except error.URLError as e:
    # 查看reason属性的对象类型
    print(type(e.reason))
    print(e.reason)
    if isinstance(e.reason, socket.timeout):
        print("Time Out!")