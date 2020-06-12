"""
注意这里的测试网站使用的百度地址，存在这样的可能性：某个代理IP能够访问百度，但是访问不了知乎，被其他人使用而导致个别网址封杀
"""
from db import RedisClient
import aiohttp
import asyncio
import time

# 定义使用代理请求的测试网站
# TEST_URL = 'http://www.baidu.com'
# TEST_URL = 'https://www.xiaoyuer.com'
TEST_URL = 'https://www.sunyuchao.com/'
# 定义访问测试网站的返回状态码
VALID_STATUS_CODES = [200, 302]
# 定义批量测试一次性检测的代理数目
BATCH_TEST_SIZE = 100


class Tester(object):
    """检测代理是否可用，使用aiohttp异步检测，提高效率"""
    def __init__(self):
        self.redis = RedisClient()

    # async代表该方法为异步方法，表明为异步请求
    async def test_single_proxy(self, proxy):
        """测试单个请求"""
        # aiohttp基于 asyncio 的异步模块,能够实现比requests更快的爬虫
        # 定义aiohttp session，类似于requests中的session对象
        conn = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            # 尝试访问测试网站
            try:
                # 注意，默认从redis数据库取出的数据是byte类型数据
                # 可以在连接redis数据库的时候加入decode_responses=True，改变返回的数据自动解码
                # 如果不加改参数，需要自行解码
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                # 重构完整proxy代理地址
                real_proxy = 'http://' + proxy
                print("正在测试", proxy)
                # 通过代理访问测试网站，异步方式访问
                async with session.get(TEST_URL, proxy=real_proxy, timeout=15) as response:
                    # 判断访问页面的返回状态码
                    if response.status in VALID_STATUS_CODES:
                        # 判断成功，即该代理可用，在redis数据库中将该代理的分数设置为最大
                        self.redis.max(proxy)
                        print("代理可用：" + proxy)
                    else:
                        # 判断失败，代理不可用，分数减1
                        self.redis.descrease(proxy)
                        print("请求返回状态码不正确：" + proxy)
             # 访问失败,代理也不可用，分数减1e
            except Exception as e:
                self.redis.descrease(proxy)
                print("代理不可用：" + proxy)

    def run(self):
        """测试主函数"""
        print("starting test!")
        try:
            # 获取所有代理
            proxies = self.redis.all()
            # 启动事件循环，监听新加入的事件循环，加以处理，不断重复，直到异步处理完成
            loop = asyncio.get_event_loop()
            # 循环遍历代理池，通过步长限定一次范围
            for i in range(0, len(proxies), BATCH_TEST_SIZE):
                # 获取第一次测试代理池范围
                test_proxies = proxies[i:i + BATCH_TEST_SIZE]
                # 根据代理组件每个代理的测试任务
                test_tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                # 将test_tasks放入事件循环，并等待所有的异步任务完成
                # 注意必须传入List对象
                loop.run_until_complete(asyncio.wait(test_tasks))
                time.sleep(5)
        except Exception as e:
            print("测试失败：", e)

if __name__ == '__main__':
    test = Tester()
    test.run()