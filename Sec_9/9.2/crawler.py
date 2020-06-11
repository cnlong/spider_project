import requests
from pyquery import PyQuery as pq
import time


class ProxyMetaclass(type):
    """元类，类似于装饰器，为继承其的类新增一些属性或者方法"""
    # 接受类名、父类、属性/方法作为参数
    def __new__(cls, name, base, attrs):
        # 新增爬取的网站的个数和其对应的爬取函数
        count = 0
        # 新增一个属性列表，记录爬取网站的函数
        # attrs是一个字典，保存着类中的属性和方法
        attrs['__CrawlFunc__'] = list()
        for k, v in attrs.items():
            # 收集爬取函数加入到新的属性列表中
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        # 爬取函数的数量
        attrs['__CrawFuncCount__'] = count
        return type(name, base, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    """代理爬取"""
    def crawl_jiangxianli(self):
        """ip.jiangxianli.com网站代理爬取"""
        # 定义起始网页,只抓取该网站中国区地址
        start_url = 'https://ip.jiangxianli.com/?page={}&country=%E4%B8%AD%E5%9B%BD'
        # 抓取前10页地址
        page_count = 10
        # 前10页地址列表
        urls = [start_url.format(page) for page in range(1, page_count+1)]
        time.sleep(3)
        for url in urls:
            try:
                print("Crawing", url)
                html = requests.get(url).content.decode('utf8')
                if html:
                    doc = pq(html)
                    # 分析网站得知地址和端口保存在table的tr中，并且第一行是表头，无需获取
                    # 获取索引大于0的所有行数据，排除第一行
                    trs = doc('tr:gt(0)').items()
                    for tr in trs:
                        # ip为每行的第一列数据
                        ip = tr.find('td:nth-child(1)').text()
                        # port为每行的第二列数据
                        port = tr.find('td:nth-child(2)').text()
                        # 合并端口和ip为完整的代理地址
                        # yield生成器返回，避免数据过大占用内存
                        yield ":".join([ip, port])
            except Exception:
                print('网页访问有误')

    def crawl_kuaidaili(self):
        """https://www.kuaidaili.com/free/inha/1/
        快代理网站爬取
        """
        start_url = 'https://www.kuaidaili.com/free/inha/{}/'
        # 抓取前10页地址
        page_count = 10
        # 前10页地址列表
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            try:
                print("Crawing", url)
                html = requests.get(url).content.decode('utf8')
                time.sleep(3)
                if html:
                    doc = pq(html)
                    # 分析网站得知地址和端口保存在table的tr中，并且第一行是表头，无需获取
                    trs = doc('tbody tr').items()
                    for tr in trs:
                        # ip为每行的第一列数据
                        ip = tr.find('td:nth-child(1)').text()
                        # port为每行的第二列数据
                        port = tr.find('td:nth-child(2)').text()
                        # 合并端口和ip为完整的代理地址
                        # yield生成器返回，避免数据过大占用内存
                        yield ":".join([ip, port])
            except Exception:
                print('网页访问有误')

    def crawl_ip66(self):
        """http://www.66ip.cn/"""
        start_url = 'http://www.66ip.cn/{}.html'
        # 抓取前10页地址
        page_count = 10
        # 前10页地址列表
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            try:
                print("Crawing", url)
                # 注意该网站的解码格式
                html = requests.get(url).content.decode('gbk')
                time.sleep(3)
                if html:
                    doc = pq(html)
                    # 分析网站得知地址和端口保存在table的tr中，并且第一行是表头，无需获取
                    # 获取索引大于0的所有行数据，排除第一行
                    trs = doc('tr:gt(0)').items()
                    for tr in trs:
                        if tr.find('td:nth-child(1)').text() != 'ip':
                            # ip为每行的第一列数据
                            ip = tr.find('td:nth-child(1)').text()
                            # port为每行的第二列数据
                            port = tr.find('td:nth-child(2)').text()
                            # 合并端口和ip为完整的代理地址
                            # yield生成器返回，避免数据过大占用内存
                            yield ":".join([ip, port])
            except Exception:
                print('网页访问有误')

    def get_proxies(self, callback):
        """
        根据爬取函数获取代理
        :param callback: 爬取函数
        :return:
        """
        proxies = list()
        # eval函数用来执行一个字符串表达式，并返回表达式的值
        for proxy in eval("self.{}()".format(callback)):
            print("成功获取代理：" + proxy)
            proxies.append(proxy)
        return proxies