from urllib.robotparser import RobotFileParser
from urllib.request import urlopen


rp = RobotFileParser()
# 将robots.txt中的内容解码分行，传入parse方法中
# 注意这里反爬虫的机制，导致获取不到这个robots.txt文件
rp.parse(urlopen('http://www.jianshu.com/robots.txt').read().decode('utf-8').split('\n'))

# 通过can_fetch方法，判断某个爬虫是否能够爬取某个页面
print(rp.can_fetch("*", "https://www.jianshu.com/p/b67554025d7d"))
