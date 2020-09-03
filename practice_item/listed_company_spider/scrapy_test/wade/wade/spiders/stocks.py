# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from urllib.parse import urlencode
from wade.items import WadeItem
from bs4 import BeautifulSoup
import pandas as pd


class StocksSpider(scrapy.Spider):
    name = 'stocks'
    allowed_domains = ['s.askci.com']
    pages = 180
    date = '2018-12-31'
    date_brif = '201812'
    url = 'http://s.askci.com/stock/a/?'
    # start_urls = ['http://s.askci.com/']

    def start_requests(self):
        for i in range(1, self.pages):
            paras = {
                'reportTime': self.date,
                'pageNum': i
            }
            self.url + urlencode(paras)
            yield Request(self.url + urlencode(paras), callback=self.parse)

    def parse(self, response):
        """解析数据"""
        # 获取响应源码
        html = response.text
        # 解析对象
        soup = BeautifulSoup(html, 'lxml')
        # 获取表格部分
        content = soup.select('#myTable04')[0]
        # 使用pd获取表格部分数据,列表形式返回，元素类型为pd的dataframe类型
        table = pd.read_html(content.prettify(), header=0)[0]
        table.rename(columns={'序号': 'serial_number', '股票代码': 'stock_code', '股票简称': 'stock_abbre', '公司名称': 'company_name',
                            '省份': 'province', '城市': 'city', '主营业务收入('+self.date_brif+')': 'main_bussiness_income',
                            '净利润('+self.date_brif+')': 'net_profit', '员工人数': 'employees', '上市日期': 'listing_date',
                            '招股书': 'zhaogushu', '公司财报': 'financial_report', '行业分类': 'industry_classification',
                            '产品类型': 'industry_type', '主营业务': 'main_business'}, inplace=True)
        das = table.to_dict(orient='records')
        for da in das:
            item = WadeItem()
            for key, value in da.items():
                item[key] = value
            yield item
