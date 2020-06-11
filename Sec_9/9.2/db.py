import redis
from random import choice

# 定义最高分、最低分、初始分
MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10
REDIS_HOST = '192.168.6.160'
REDIS_PORT = 6379
REDIS_KEY = 'proxies'
REDIS_DB = 1

class RedisClient(object):
    """Redis数据库客户端"""
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB):
        """
        初始化连接
        :param host: Redis地址
        :param port: Redis端口
        :param db: 连接的库
        """
        self.sr = redis.StrictRedis(host=host, port=port, db=db)

    def add(self, proxy, score=INITIAL_SCORE):
        """添加新代理"""
        # 判断库中是否存在该代理
        if not self.sr.zscore(REDIS_KEY, proxy):
            self.sr.zadd(REDIS_KEY, score, proxy)

    def random(self):
        """随机获取最高分代理，如果不存在，就按照排名获取"""
        # 获取最高分代理
        result = self.sr.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        # 判断是否获取到最高分代理
        if len(result):
            # 随机返回一个代理
            return choice(result)
        else:
            # 未获取到最高分代理，则按照排名来获取代理
            # zrevrange按照权重值从大到小排序
            result = self.sr.zrevrange(REDIS_KEY, MIN_SCORE, MAX_SCORE)
            if len(result):
                return choice(result)
            else:
                raise SystemExit("未获取到任何可用代理")

    def descrease(self, proxy):
        """代理减分，分数小于最低值时从数据库中移除"""
        # 根据代理获取其权重值
        score = self.sr.zscore(REDIS_KEY, proxy)
        # 如果获取到值，且大于最小值，则减1
        if score and score > MIN_SCORE:
            print('代理：'+ proxy + '当前分数：'+ score + '减1' )
            return self.sr.zincrby(REDIS_KEY, proxy, -1)
        # 如果小于最小值，移除
        else:
            print('代理：' + proxy + '当前分数：' + score + '移除')
            return self.sr.zrem(REDIS_KEY, proxy)

    def exist(self, proxy):
        """判断某个代理是否存在"""
        score = self.sr.zscore(REDIS_KEY, proxy)
        # 查到socre为值，查不到socre为None
        # score == None
        # 存在not false返回true
        # 不存在not ture 返回false
        return not score == None

    def max(self, proxy):
        """一旦某个代理可用，即将其分数设置为最大值"""
        print("代理" + proxy + '可用，设置为：'+ MAX_SCORE)
        return self.sr.zadd(REDIS_KEY, MAX_SCORE, proxy)

    def count(self):
        """获取代理的数量"""
        return self.sr.zcard(REDIS_KEY)

    def all(self):
        """获取全部代理"""
        return self.sr.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)
