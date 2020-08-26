# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import json
import logging
import requests


class WeiboSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class WeiboDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ProxyMiddleware(object):
    """设置代理的DownloaderMiddleware"""
    def __init__(self, proxy_url):
        # 日志收集器,用类名作为logger的名字
        self.logger = logging.getLogger(__name__)
        # 获取代理的url
        self.proxy_url = proxy_url

    def get_random_proxy(self):
        """根据代理url，随机获取一个代理"""
        try:
            response = requests.get(self.proxy_url)
            if response.status_code == 200:
                proxy = response.text
                return proxy
        # 代理池url请求超时
        except requests.ConnectionError:
            return False

    @classmethod
    def from_crawler(cls, crawler):
        # 从spider的配置文件中获取代理池地址
        return cls(proxy_url=crawler.settings.get('PROXY_URL'))

    def process_request(self, request, spider):
        """注意这里需要返回None，只为其添加代理，添加cookie方法类似"""
        # 这里赋值代理的判断条件是当前的retry_times不为空，也就是在第一次请求失败的时候才启用代理
        if request.meta.get('retry_times'):
            proxy = self.get_random_proxy()
            if proxy:
                # 构建代理完整地址
                uri = 'https://{proxy}'.format(proxy=proxy)
                # 记录日志
                self.logger.debug('使用代理：' + uri)
                # 给request增加代理
                request.meta['proxy'] = uri
                # 注意这里必须返回NONE


class CookiesMiddleware(object):
    """赋予Cookie"""
    def __init__(self, cookies_url):
        self.logger = logging.getLogger(__name__)
        self.cookies_url = cookies_url

    def get_random_cookies(self):
        try:
            response = requests.get(self.cookies_url)
            if response.status_code == 200:
                cookies = response.text
                return cookies
        except requests.ConnectionError:
            return False

    @classmethod
    def from_crawler(cls, crawler):
        return cls(cookies_url=crawler.settings.get('COOKIES_URL'))

    def process_request(self, request, spider):
        # cookies = self.get_random_cookies()
        cookies = {"WEIBOCN_FROM":"1110006030", "SCF":"Aub_3DcoAvaDm7Sf-qQCtFKI53t37IPq0JV1fpRWkzfxj0oFwtkebigYdjL1xYSyVl42glYQ_FHfvIeLrQvjrEU.;","SUB":"_2A25yL-_PDeRhGeNL41UQ8yfFzDqIHXVR0_GHrDV6PUNbktANLUWmkW1NSMDjJaJo_CoA2M1pERH1I3f5QzV-S6QR","SUBP":"0033WrSXqPxfM725Ws9jqgMF55529P9D9W5IyOFUf3sEpkOHzb_T22CB5JpX5KzhUgL.Fo-f1hMpe0.4S0q2dJLoI0YLxK-LBKqLBoeLxKMLB-eL1K2LxKqL1hnL1K2LxK.L1K.LB-2LxKML1-BL1h5LxK-LBKqLBoeLxKMLB-eL1K2t", "SUHB":"0laVliWfAFVckW", "SSOLoginState":"1596694431", "ALF":"1599286431", "MLOGIN":"1", "_T_WM":"25173663288", "XSRF-TOKEN":"329f10", "M_WEIBOCN_PARAMS":"luicode%3D10000011%26lfid%3D231051_-_recomgroupmemberlist_-_3708997377132149_-_1674166903_-_2310511063_1_3.0_5587139976_3708997377132149_d6374089%26fid%3D1076032151457574%26uicode%3D10000011"}
        if cookies:
            requests.cookies = cookies
            self.logger.debug('使用cookies' + json.dumps(cookies))