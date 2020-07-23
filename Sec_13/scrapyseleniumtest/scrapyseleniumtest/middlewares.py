# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
from logging import getLogger
from selenium.webdriver.chrome.options import Options


class ScrapyseleniumtestSpiderMiddleware(object):
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


class ScrapyseleniumtestDownloaderMiddleware(object):
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


class SeleniumMiddleware(object):
    """调用Selenium处理抓取请求"""
    def __init__(self, timeout=None, driverpath=None):
        self.driver_path = driverpath
        self.logger = getLogger(__name__)
        self.timeout = timeout
        # 利用chrome的无头浏览模式
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-gpu')
        self.browser = webdriver.Chrome(options=self.chrome_options, executable_path=self.driver_path)
        self.browser.set_window_size(1400, 700)
        self.browser.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.browser, self.timeout)

    def __del__(self):
        """此类对象关闭的时候操作,因为是无头浏览模式，需要手动关闭"""
        self.browser.close()

    def process_request(self, request, spider):
        """
        Chrome无头抓取
        :param request: Request对象
        :param spider:  Spider对象
        :return: HtmlResponse
        """
        # 记录日志
        self.logger.debug('Chrome is Starting')
        # 获取此时请求的页码。首次请求没有页码设定默认值为1
        page = request.meta.get('page', 1)
        try:
            # 抓取网页
            self.browser.get(request.url)
            # 注意上一步，请求的是首页，如果request中有传入页码数，还需要在浏览器上页码块进行转页
            if page > 1:
                # 获取转页输入框
                input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))
                # 获取转页确定按钮
                submit = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form span.btn.J_Submit')))
                # 清除输入框中的原始页码
                input.clear()
                # 输入request中传入的页码
                input.send_keys(page)
                # 点击确定按钮跳转
                submit.click()
            # 等待网页加载
            # 1.网页中所有的淘宝商品信息加载完成
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
            # 2.当前页显示的页码和传入的页码一致
            self.wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), str(page)))
            # 页码加载完成，返回HtmlResponse给Spider
            # self.browser.page_source获取浏览器加载后的源码
            return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8', status=200)
        except TimeoutException:
            # 请求超时或者加载超时,返回500状态码
            return HtmlResponse(url=request.url, status=500, request=request)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'),
                   driverpath=crawler.settings.get('SELENIUM_DRIVER_PATH'))