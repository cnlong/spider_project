import requests
from requests import Request, Session
# dunmps序列化，loads反序列化
from pickle import dumps, loads
from redis import StrictRedis
from urllib.parse import urlencode
from pyquery import PyQuery as pq



PROXY_POOL_URL = 'http://127.0.0.1:5000/random'
REDIS_KEY = 'weixinrequest'


class WeiXinRequest(Request):
    """继承自Request，构造自定义的Request对象，加入自定义的属性方法"""
    def __init__(self, url, callback, method='Get', headers=None, need_proxy=False, fail_time=0, timeout=10):
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


class RedisQueue(object):
    """redis队列存储类"""
    def __init__(self):
        """初始化redis"""
        self.db = StrictRedis(host='192.168.6.160', port=6379, db= 2)

    def add(self, request):
        """向队列添加序列化后的Request对象"""
        # 判断该请求是否为新建的weixin的Requst对象
        if isinstance(request, WeiXinRequest):
            return self.db.rpush(REDIS_KEY, dumps(request))
        return False

    def pop(self):
        """取出一个Request对象，并反序列化"""
        # 判断队列中是否存在请求对象
        if self.db.llen(REDIS_KEY):
            # lpop 命令用于移除并返回列表的第一个元素
            # 因为模拟队列操作，取出该请求对象之后，其在使用过程中不该再出现在队列中
            return loads(self.db.lpop(REDIS_KEY))
        else:
            return False

    def empty(self):
        """判断队列是否为空"""
        return self.db.llen(REDIS_KEY) == 0


class Spider(object):
    """利用此前创建的weixinrequesr对象构建完整的爬虫请求（请求头，代理地址，回调函数），加入redis队列"""
    def __init__(self):
        self.base_url = 'https://weixin.sogou.com/weixin'
        self.keyword = 'NBA'
        # 注意，这里的cookies等信息，使用浏览器登录账户后的信息
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN, zh;q=0.9',
            'Connection': 'keep-alive',
            'cookie': 'CXID=55E066FBDF296CE815E62232E7C02B4F; SUID=BA31E2DD4C238B0A5D494F1E000F2530; wuid=AAEteKVrLgAAAAqLFD0gCA0AGwY=; IPLOC=CN3201; ld=KZllllllll2WeLCVlllllVE4bUUlllllTWwemkllll9lllllVklll5@@@@@@@@@@; ABTEST=8|1592359054|v1; weixinIndexVisited=1; SUV=000A2C4EDDE231BA5EE97890EA290113; SNUID=A42FFCC01E18B5200BA4D33B1E9AE9DC; JSESSIONID=aaaX1ddA43yQjd78Onxix; sct=2; ppinf=5|1592375086|1593584686|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToyNzolRTUlQjAlOEYlRTclOTklQkQlRTklQkUlOTl8Y3J0OjEwOjE1OTIzNzUwODZ8cmVmbmljazoyNzolRTUlQjAlOEYlRTclOTklQkQlRTklQkUlOTl8dXNlcmlkOjQ0Om85dDJsdU04Zkd0T2t3RWRNbVZIWFRRNHIwSmtAd2VpeGluLnNvaHUuY29tfA; pprdig=bryAAGm0fnV3ue259VOx3D5r6xih6B2ZEXggfyY9b66pLJaOmpJxbF1VL2t84gUHY0cYALwmqO1EcUvWjuzyvinv2PneB0Ronmk8JWOcR_V0Ke0IiGT0V4z-u3eaRw9TztTHWm72urgUY_Fv1_iG9RmNLWGL1eCkQW3uPHozRvw; sgid=06-46429453-AV7pty7utlKH56ibZ7by7d7U; ppmdig=159237508600000073419360b6cdd786606a9b35122d8c79',
            'Host': 'weixin.sogou.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
        }
        # 创建session对象，同session下的发出请求共用cookies等参数
        self.session = Session()
        # redis队列
        self.queue = RedisQueue()

    def get_proxy(self):
        """获取代理"""
        try:
            response = requests.get(PROXY_POOL_URL)
            if response.status_code == 200:
                print("Get proxy:", response.text)
                return response.text
            # 没有可用代理返回None
            return None
        # 代理网站访问失败返回None
        except requests.ConnectionError:
            return None

    def parse_index(self, response):
        """解析索引页"""
        # 此时的response是访问搜索结果后返回的内容
        doc = pq(response.text)
        # 找出页面中的每个文章块
        items = doc('.news-box .news-list li .txt-box h3 a').items()
        for item in items:
            # 获取每个文章块的链接属性，构建新的weixinReqauest对象
            url = item.attr('href')
            weixin_request = WeiXinRequest(url=url, callback=self.parse_detail)
            yield weixin_request
        # 获取下一页按钮的跳转url地址
        next = doc('#sogou_next').attr('href')
        if next:
            # 构建完整的下一页url请求地址
            url = self.base_url + str(next)
            # 下一页的链接地址构建一个新的request对象
            weixin_request = WeiXinRequest(url=url, callback=self.parse_index, need_proxy=True)
            yield weixin_request

    def parse_detail(self, response):
        """解析每个文章的详情信息"""
        # 此时的response是每篇文章的url返回的结果
        doc = pq(response.text)
        # 解析网页，获取具体的信息，组成字典
        data = {
            'title': doc('.rich_media_title').text(),
            'content': doc('.rich_media_content').text(),
            'date': doc('#publish_time').text(),
            # 注意部分元素块是隐藏的，需要分析网站源码获取
            'nickname': doc('#js_profile_qrcode > div > strong').text(),
            'wechat': doc('#js_profile_qrcode > div > p:nth-child(3) > span').text()
        }
        yield data

    def start(self):
        """初始化第一个查询的url地址"""
        # 全局更新Headers
        self.session.headers.update(self.headers)
        # 构建第一个请求的url地址
        start_url = self.base_url + '?' + urlencode({'query': self.keyword, 'type': 2})
        # 构建request对象
        # 回调函数使用文章列表页的处理函数
        weixin_request = WeiXinRequest(url=start_url, callback=self.parse_index, need_proxy=True)
        # 将第一个请求放入队列，等待调度
        self.queue.add(weixin_request)

