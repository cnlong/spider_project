import requests

proxy = '113.101.151.171:4216'
proxies = {
    'http': 'http://' + proxy,
    'https': 'https://' + proxy
}
try:
    response = requests.get('http://httpbin.org/get', proxies=proxies)
    print(response.text)
except requests.exceptions.ConnectionError as e:
    print(e)