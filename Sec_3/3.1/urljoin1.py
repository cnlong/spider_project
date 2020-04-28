from urllib.parse import urljoin

print(urljoin('http://www.baidu.com', 'FAQ.html'))
print(urljoin('http://www.baidu.com', 'https://www.baidu.com/FAQ.html'))
print(urljoin('http://www.baidu.com?wd=abdc', 'https://www.baidu.com/FAQ.html'))