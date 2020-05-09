from bs4 import BeautifulSoup

html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters;and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Elsie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
    and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""
# 定义BeautifulSoup对象，并传入HTML文档和解析器
# 注意这里会对HTML文档进行自动更正，补全缺失节点
soup = BeautifulSoup(html, 'lxml')
# 以标准的缩进格式输出
print(soup.prettify())
print(soup.title.string)