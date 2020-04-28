from urllib.robotparser import RobotFileParser

# 声明类的实例对象
rp = RobotFileParser()
# 传入robots.txt链接
rp.set_url('https://www.jianshu.com/robots.txt')
# 读取robots文件进行分析，必须要做的操作
rp.read()
# 通过can_fetch方法，判断某个爬虫是否能够爬取某个页面
print(rp.can_fetch("*", "https://www.jianshu.com/p/b67554025d7d"))
