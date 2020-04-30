import requests

headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
}
r = requests.get('https://www.zhihu.com/explore', headers=headers)
print(r.text)