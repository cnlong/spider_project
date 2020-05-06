import requests

# 设置代理
proxies = {
    "http": "http://10.10.1.10:3128",
    "https": "http://10.10.1.10:1080"
}

# 如果代理需要密码认证，就可以按照以下方式传入密码和用户名
proxies2 = {
    "http": "http://user:password@10.10.1.10:3128",
    "https": "http://user:password@10.10.1.10:1080"
}
requests.get('https://www.taobao.com', proxies=proxies)