from urllib.parse import quote

keyword = '壁纸'
url = 'http://www.baidu.com/s?wd=' + quote(keyword)
print(url)