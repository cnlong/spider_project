from db import RedisClient
from crawler import Crawler


# 定义代理池的地址上线范围
POOL_UPPER_THRESHOLD = 10000
class Getter(object):
    def __init__(self):
        """初始化redis连接和爬取"""
        self.redis = RedisClient()
        self.crawler =Crawler()

    def is_over_threshold(self):
        """判断代理池地址数量是否超过上线"""
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def run(self):
        """获取代理并存入数据库"""
        print("开始执行")
        if not self.is_over_threshold():
            # 遍历爬取函数数量，即为对应爬取函数的索引值
            for callback_label in range(self.crawler.__CrawFuncCount__):
                # 获取对应索引的爬取函数
                callback = self.crawler.__CrawlFunc__[callback_label]
                # 获取代理
                proxies = self.crawler.get_proxies(callback)
                # 存储代理
                for proxy in proxies:
                    self.redis.add(proxy)


if __name__ == '__main__':
    getter = Getter()
    getter.run()