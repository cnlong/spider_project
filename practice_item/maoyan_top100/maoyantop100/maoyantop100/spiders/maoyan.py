# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from bs4 import BeautifulSoup
from maoyantop100.items import Maoyantop100Item


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    # start_urls = ['http://maoyan.com/']
    pages = 10
    url = 'https://maoyan.com/board/4?offset={num}'
    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
    }
    # 设置cookies
    cookies = {
        "__mta": "246838843.1599117046221.1599119154317.1599119416689.14", "uuid_n_v": "v1",
        "uuid": "920B1F00EDB411EA851A952F943E020F95EF9936AEA04497AFBC93DEE9A08EBC",
        "_csrf": "ae4f879053a07c819fb8dfc5d6575cbf25482674d700b4e6a8bfa5fe66b73a9f",
        "_lxsdk_cuid": "17452cdafe1c8-0c1c301ff25d1a-3c3f5a0c-15f900-17452cdafe1c8",
        "_lxsdk": "920B1F00EDB411EA851A952F943E020F95EF9936AEA04497AFBC93DEE9A08EBC",
        "Hm_lvt_703e94591e87be68cc8da0da7cbd0be2": "1599117046", "mojo-uuid": "41fcc792e68782a44a1e6a33daaaa99b",
        "mojo-session-id": '{"id":"a3a14dfa41eabe0db871103180e17118","time":1599117046295}',
        "__mta": "246838843.1599117046221.1599117072878.1599117241051.3", "mojo-trace-id": "30",
        "Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2": "1599119417", "_lxsdk_s": "17452cdafe3-186-f4c-ab1%7C%7C47"
    }

    def start_requests(self):
        for page in range(1, self.pages + 1):
            num = (page - 1) * 10
            url = self.url.format(num=num)
            yield Request(url=url, callback=self.parse, headers=self.headers, cookies=self.cookies)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        # 每个页面展示10个电影，每个电影的布局基本一致
        for i in range(10):
            item = Maoyantop100Item()
            # 使用class_避免与Python中的class冲突
            item['index'] = soup.find_all(class_='board-index')[i].string
            item['thumb'] = soup.find_all(class_='board-img')[i].attrs['data-src']
            item['name'] = soup.find_all(name='p', attrs={'class':'name'})[i].string
            item['star'] = soup.find_all(name='p', attrs={'class': 'star'})[i].string.strip()
            item['area'] = soup.find_all(class_='releasetime')[i].string.strip()
            item['time'] = soup.find_all(class_='releasetime')[i].string.strip()
            item['score'] = soup.find_all(name='i', attrs={'class':'integer'})[i].string.strip() + soup.find_all(name='i', attrs={'class':'fraction'})[i].string.strip()
            yield item

