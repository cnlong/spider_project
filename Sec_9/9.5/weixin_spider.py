"""
目前代码不完善，爬取过程提示302，应该是访问次数过多，需要输入验证码解封
1.更换代理，但是发现更换代理之后也还是无法解决这个问题
2.识别验证码破解，需要用到selenium，代码需要做大变动
"""
import requests
from requests import Request, Session, ReadTimeout, ConnectionError
# dunmps序列化，loads反序列化
from pickle import dumps, loads
from redis import StrictRedis
from urllib.parse import urlencode
from pyquery import PyQuery as pq
import pymysql



PROXY_POOL_URL = 'http://127.0.0.1:5000/random'
REDIS_KEY = 'weixinrequest'
VALID_STATUS = [200]
MAX_FAILED_TIME = 20
MYSQL_HOST = '192.168.6.160'
MYSQL_USER = 'root'
MYSQL_PASSWORD = '123456'
MYSQL_PORT = 3306
MYSQL_DATABASE = 'weixin'




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


class Mysql(object):
    """MySQL连接"""
    def __init__(self, host=MYSQL_HOST, username=MYSQL_USER, password=MYSQL_PASSWORD,
                 port=MYSQL_PORT, database=MYSQL_DATABASE):
        """初始化数据库连接"""
        try:
            self.db = pymysql.connect(host, username, password, database,
                                      charset='utf8', port=port)
            self.cursor = self.db.cursor()
        except pymysql.MySQLError as e:
            print(e.args)

    def insert(self, table, data):
        """数据插入"""
        # 构建sql语句
        keys = ','.join(data.keys())
        values = ','.join(['%s'] * len(data))
        sql_query = 'insert into %s (%s) values (%s)' % (table, keys, values)
        try:
            self.cursor.execute(sql_query, tuple(data.values()))
            self.db.commit()
        except pymysql.MySQLError as e:
            print(e.args)


class RedisQueue(object):
    """redis队列存储类"""
    def __init__(self):
        """初始化redis"""
        self.db = StrictRedis(host='192.168.6.160', port=6379)

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
    # 注意这边不能使用init方法定义对象属性，否则会提示进程锁定对象的
    # 类似多个进程之间共享数据时候，会锁定数据
    # 采用类属性的就可以避免
    # def __init__(self):
    base_url = 'https://weixin.sogou.com/weixin'
    keyword = 'NBA'
    # 注意，这里的cookies等信息，使用浏览器登录账户后的信息
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN, zh;q=0.9',
        'Connection': 'keep-alive',
        'cookie': 'CXID=55E066FBDF296CE815E62232E7C02B4F; SUID=BA31E2DD4C238B0A5D494F1E000F2530; wuid=AAEteKVrLgAAAAqLFD0gCA0AGwY=; IPLOC=CN3201; ld=KZllllllll2WeLCVlllllVE4bUUlllllTWwemkllll9lllllVklll5@@@@@@@@@@; ABTEST=8|1592359054|v1; weixinIndexVisited=1; SUV=000A2C4EDDE231BA5EE97890EA290113; SNUID=A42FFCC01E18B5200BA4D33B1E9AE9DC; JSESSIONID=aaaX1ddA43yQjd78Onxix; sct=2; ppinf=5|1592375086|1593584686|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToyNzolRTUlQjAlOEYlRTclOTklQkQlRTklQkUlOTl8Y3J0OjEwOjE1OTIzNzUwODZ8cmVmbmljazoyNzolRTUlQjAlOEYlRTclOTklQkQlRTklQkUlOTl8dXNlcmlkOjQ0Om85dDJsdU04Zkd0T2t3RWRNbVZIWFRRNHIwSmtAd2VpeGluLnNvaHUuY29tfA; pprdig=bryAAGm0fnV3ue259VOx3D5r6xih6B2ZEXggfyY9b66pLJaOmpJxbF1VL2t84gUHY0cYALwmqO1EcUvWjuzyvinv2PneB0Ronmk8JWOcR_V0Ke0IiGT0V4z-u3eaRw9TztTHWm72urgUY_Fv1_iG9RmNLWGL1eCkQW3uPHozRvw; sgid=06-46429453-AV7pty7utlKH56ibZ7by7d7U; ppmdig=15924597680000007e22e348674ba594b514f1b3d70f67c8',
        'Host': 'weixin.sogou.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
    }
    # 创建session对象，同session下的发出请求共用cookies等参数
    session = Session()
    # redis队列
    queue = RedisQueue()
    # MySql
    mysql = Mysql()

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

    def request(self, weixin_request):
        """执行request的方法"""
        try:
            # 判断请求是否需要代理
            # 默认请求不需要代理，需要特殊指定
            # 第一个查询请求和后续的翻页请求都需要新的代理
            # 而同一个请求下的子页面的请求共用session无需代理
            if weixin_request.need_proxy:
                proxy = self.get_proxy()
                if proxy:
                    # 构建代理
                    proxies = {
                        'http': 'http://' + proxy,
                        'https': 'https://' + proxy
                    }
                    # 发送请求
                    # allow_redirects=True 禁止重定向
                    response = self.session.send(weixin_request.prepare(), timeout=weixin_request.timeout,
                                             allow_redirects=False, proxies=proxies)
                    print(response.status_code)
                    return response
            # 无需代理，直接请求
            response = self.session.send(weixin_request.prepare(),timeout=weixin_request.timeout,
                                             allow_redirects=False)
            print(response.status_code)
            return response
        except (ConnectionError, ReadTimeout) as e:
            print(e.args)
            return False

    def schedule(self):
        """从队列调度请求"""
        # 只要队列不为空，就一直调度
        while not self.queue.empty():
            # 从第一个请求开始获取
            weixin_request = self.queue.pop()
            print(weixin_request)
            # 索引页面的请求的回调函数都是对应索引的页面分析函数
            # 每篇文章的请求的回调函数都是对应详情页分析函数
            callback = weixin_request.callback
            # 获取当前请求地址
            print("Schedule:", weixin_request.url)
            # 获取请求结果
            response = self.request(weixin_request)
            # 判断请求结果及状态码
            if response and response.status_code in VALID_STATUS:
                # 调用回调函数，处理结果
                # 索引页，则返回每个文章的请求对象和下一页的请求对象
                # 详情页，则返回每篇文章的所需要的结果
                results = list(callback(response))
                if results:
                    for result in results:
                        # 判断返回的结果是请求对象还是数据字典
                        print("New Resutl:", result)
                        if isinstance(result, WeiXinRequest):
                            self.queue.add(result)
                        if isinstance(result, dict):
                            self.mysql.insert('articles', result)
                else:
                    self.error(weixin_request)
            else:
                self.error(weixin_request)

    def error(self, weixin_request):
        """报错处理，错误一次，将其失败次数加1"""
        weixin_request.fail_time = weixin_request.fail_time + 1
        print("Request Failed:", weixin_request.fail_time, 'Times', weixin_request.url)
        if weixin_request.fail_time < MAX_FAILED_TIME:
            # 失败次数大于阈值，则丢弃该请求，即不重新放回queue中循环
            # 而次数仍在阈值内的请求，失败之后，重新放回queue中循环
            self.queue.add(weixin_request)

    def run(self):
        """开始总函数"""
        self.start()
        self.schedule()


if __name__ == '__main__':
    weixin_spider = Spider()
    weixin_spider.run()