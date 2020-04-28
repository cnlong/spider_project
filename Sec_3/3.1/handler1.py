from urllib.request import HTTPBasicAuthHandler, HTTPPasswordMgrWithDefaultRealm, build_opener
from urllib.error import URLError

username = 'username'
password = 'password'
url = 'http://localhost:5000'

# 构建密码声明，用于维护密码和用户名
p = HTTPPasswordMgrWithDefaultRealm()
# 添加用户名密码url
p.add_password(None, url, username, password)
# 创建认证处理器，并传入上面创建的密码管理器
auth_handler = HTTPBasicAuthHandler(p)
# 创建opener,可以通过其发送请求
opener = build_opener(auth_handler)

# 请求网页
try:
    # 通过opener的open()方法打开链接，就可以发送一个带有验证的请求
    res = opener.open(url)
    html = res.read().decode('utf-8')
    print(html)
except URLError as e:
    print(e.reason)
