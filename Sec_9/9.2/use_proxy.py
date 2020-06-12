"""代理池创建完成，其他普通用户即可访问api接口获取随机代理地址并使用"""
import requests


PROXY_POOL_URL = 'http://127.0.0.1:5000/random'


def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None


proxy = "112.253.11.113:8000"
proxies = {
    'http': 'http://' + proxy,
    'https': 'https://' + proxy,
}

try:
    response = requests.get('http://httpbin.org/get', proxies=proxies)
    print(response.text)
except requests.exceptions.ConnectionError as e:
    print("Error:", e.args)