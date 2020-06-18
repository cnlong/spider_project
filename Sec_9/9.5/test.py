import requests
from requests import Request, Session, ReadTimeout, ConnectionError
# dunmps序列化，loads反序列化
from pickle import dumps, loads
from redis import StrictRedis
from urllib.parse import urlencode
from pyquery import PyQuery as pq
import pymysql


class WeiXinRequest(Request):
    """继承自Request，构造自定义的Request对象，加入自定义的属性方法"""
    def __init__(self, url, callback, method='GET', headers=None, need_proxy=False, fail_time=0, timeout=10):
        # 调用父类的初始化方法
        Request.__init__(self, method, url, headers)
        # 定义自定义的属性
        # 回调函数，获取该请求的响应结果
        self.callback = callback
        # 是否需要代理爬取
        self.need_proxy = need_proxy
        # 失败次数，超过阈值，从队列中移除
        self.fail_time = fail_time
        # 超时时间
        self.timeout = timeout

url = 'https://weixin.sogou.com/weixin?query=NBA&type=2'
weixin = WeiXinRequest(url=url, callback=None)

proxy = '120.55.97.83:80'
proxies = {
                        'http': 'http://' + proxy,
                        'https': 'https://' + proxy
                    }
session = Session()
response = session.send(weixin.prepare(), timeout=10,
                         allow_redirects=False, proxies=proxies)


print(response.text)