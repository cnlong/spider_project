import random
import redis
from .settings import *


class RedisClient(object):
    """redis数据库类"""
    def __init__(self, datatype, website, host=REDIS_HOST, port=REDIS_PORT):
        """
        初始化连接
        :param datatype: 类型，密码或者cookies
        :param website: 网站名称
        :param host: redis地址
        :param port: redis端口
        """
        self.db = redis.StrictRedis(host=host, port=port, decode_responses=True)
        self.type = datatype
        self.website = website

    def name(self):
        """根据类型和网站，获取hash的名称"""
        return "{type}:{website}".format(type=self.type, website=self.website)

    def set(self, username, value):
        """设置键值对"""
        return self.db.hset(self.name(), username, value)

    def get(self, username):
        """获取键值对"""
        return self.db.hget(self.name(), username)

    def delete(self, username):
        """根据键名删除键值对"""
        return self.db.hdel(self.name(), username)

    def count(self):
        """获取键值对数量"""
        return self.db.hlen(self.name())

    def random(self):
        """随机获取一个键值对"""
        # havls获取hash表中所有的域对应的值
        return random.choice(self.db.hvals(self.name()))

    def usernames(self):
        """获取所有账户信息"""
        # hkeys获取hash表中所有的域
        return self.db.hkeys(self.name())

    def all(self):
        """获取所有的域值对"""
        return self.db.hgetall(self.name())
