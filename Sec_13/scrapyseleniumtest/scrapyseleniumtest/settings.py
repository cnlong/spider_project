# -*- coding: utf-8 -*-

# Scrapy settings for scrapyseleniumtest project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'scrapyseleniumtest'

SPIDER_MODULES = ['scrapyseleniumtest.spiders']
NEWSPIDER_MODULE = 'scrapyseleniumtest.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scrapyseleniumtest (+http://www.yourdomain.com)'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True
# 不遵守robots协议爬取
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'scrapyseleniumtest.middlewares.ScrapyseleniumtestSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'scrapyseleniumtest.middlewares.ScrapyseleniumtestDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'scrapyseleniumtest.pipelines.ScrapyseleniumtestPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# selenium超时时间
SELENIUM_TIMEOUT = 50

PHANTOMJS_ARGS = ['--load-images=false', '--disk-cache=true']

# 爬取页码
MAX_PAGE = 3
# 爬取关键字
KEYWORDS = ['iPad']
# chrome驱动位置
SELENIUM_DRIVER_PATH = r'E:\python_project\spider_project\venv\Scripts\chromedriver'

# 添加自定义的Downloader Middleware
DOWNLOADER_MIDDLEWARES = {
    'scrapyseleniumtest.middlewares.SeleniumMiddleware': 543,
}

# 配置headers信息
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
    'cookie': 'cna=V9WYFXi6fSICAd3iMbqVN5eq; miid=827204541033267410; cookie2=1afebbaff6cd7504a2ec6ef76074c9b4; _tb_token_=fb3bf3b376b8e; v=0; thw=cn; tg=0; t=2d8627aa40d79f95095235cd73725fe1; _samesite_flag_=true; alitrackid=www.taobao.com; hng=CN%7Czh-CN%7CCNY%7C156; tk_trace=oTRxOWSBNwn9dPyorMJE%2FoPdY8zZPEr%2FCrvCMS%2BG3sTRRWrQ%2BVVTl09ME1KrU%2BU98S7W2O%2FKmxQs8Yi%2BF2PRZZ8yPoKoskEH2UmaSffUcIMH8hie%2BIBMVCRFIFzsv6%2BmPZ1AvRrNw3Fo8cmM9mCyQNIzVxNPD9DaSBjbzpSv3gkbaSmnMjvoGLAJpEAGVR497Nz0s5ozF9XDLQfc7XVezT%2ByXIMDRPe8XeWg5nIxHTip1L3%2FRlyp74oj4JqZeN5Dmfz2N%2FgZPpnCVsD6tgpC7yfwYqtzZaoiR8aZNy18Q5uYSumOpntDoxziJWreNdTztEAAPJzElbVw6rvk; mt=ci%3D-1_1; sgcookie=EBg4JfRZM4snzoQZ7fpFS; unb=1636774851; uc1=tag=10&cookie14=UoTV6ei4Bxk6RA%3D%3D&cookie15=UIHiLt3xD8xYTw%3D%3D&pas=0&existShop=false&cookie21=W5iHLLyFeYZ1WM9hVnmS&cookie16=UIHiLt3xCS3yM2h4eKHS9lpEOw%3D%3D&lng=zh_CN; uc3=nk2=sym3AVyG25I%3D&id2=Uoe3cckJsQ%2FrGQ%3D%3D&lg2=W5iHLLyFOGW7aA%3D%3D&vt3=F8dBxGygRD9ZyGRIQLA%3D; csg=d90f3392; lgc=%5Cu5C0F%5Cu80D6%5Cu7231%5Cu6668; cookie17=Uoe3cckJsQ%2FrGQ%3D%3D; dnk=%5Cu5C0F%5Cu80D6%5Cu7231%5Cu6668; skt=c087aac0d2af10bf; existShop=MTU5NTU3Njg2Mw%3D%3D; uc4=nk4=0%40sVYX%2F3bFTMoPDFuF1QV8KXKRrw%3D%3D&id4=0%40UO%2BxLH98Ga1cn3zXFKHs0FhY9PFM; tracknick=%5Cu5C0F%5Cu80D6%5Cu7231%5Cu6668; _cc_=W5iHLLyFfA%3D%3D; _l_g_=Ug%3D%3D; sg=%E6%99%A81e; _nk_=%5Cu5C0F%5Cu80D6%5Cu7231%5Cu6668; cookie1=B0OoviOVnqxokXaYnqeAS608IhHCULtFEwJFN22eVtg%3D; enc=J10Zm3GB8W0lQNLYxLNvR50mKt0hhVPDkzzw8zKIilGCcGk7QlwAoe5JBqK9jtnHHYJZlH2u0Lo6ix2OCZfp9A%3D%3D; lastalitrackid=login.taobao.com; tfstk=cVsVBQgPmoE4uBK_JntZcS_L1qyAaPIhXuJeowKK9MVac48DTsXi6L0rpTWw9uYc.; JSESSIONID=CF762ED59AC0EA4173763369481FB857; isg=BNjYdEocM6HckB78R2_ic7thqQZqwTxLDF9OChLJHJPGrXmXu9M926HP5eWdvfQj; l=eBQlye17QZCd9XuyBOfwlurza77tJIRfguPzaNbMiOCPOACe5SHlWZkN6fLwCnGVHs9eJ3-hFr9zBW81fyCqJxpsw3k_J_DmndC..'
}