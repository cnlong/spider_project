from urllib.error import URLError
from urllib import request
import socket
# 安装pysocks
import socks

socks.set_default_proxy(socks.SOCKS5, '183.166.253.239', 6666)
socket.socket = socks.socksocket
try:
    response = request.urlopen('http://httpbin.org/get')
    print(response.read().decode('utf-8'))
except URLError as e:
    print(e.reason)