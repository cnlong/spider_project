"""
自定义爬取多个页面，年中报中存在7种类型的表格，并且报表中存在多个时间段的
可以从多个维度去爬取任意时期、任意类型的数据
根据用户的输入重新构造不同的URL
http://data.eastmoney.com/bbsj/202006/yjkb.html
"""
import time
import os
import csv
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import threading


def get_userdata():
    # 自定义报表类型的输入
    # 报表类型
    tables = int(input('请选择查询的报表类型号：'
                       '1.业绩报表'
                       '2.业绩快报'
                       '3.业绩预告'
                       '4.预约披露时间'
                       '5.资产负载表'
                       '6.利润表'
                       '7.现金流量表：'))
    while tables > 7 or tables < 1:
        tables = int(input('请输入正确的报表类型号：'))
    table_dict = {1: 'yjbb', 2: 'yjkb', 3: 'yjyg', 4: 'yysj', 5: 'zcfz', 6: 'lrb', 7: 'xjll'}
    category = table_dict[tables]

    # 自定义报表查询年限
    year = int(input('请输入要查询的年份（2009-2020）：'))
    while year > 2020 or year < 2009:
        year = int(input('请输入正确的年份：'))

    # 自定义报表查询的季度
    # 第一季度，年中报，第三季度，年报
    quarter = int(input('请输入季报类型：'
                        '1.第一季度'
                        '2.年中报'
                        '3.第三季度'
                        '4.年报：'))
    while quarter > 4 or quarter < 1:
        quarter = int(input('请输入正确的季报类型：'))
    # 转换季度类型为URL中使用的类型，03, 06, 09, 12
    # %02d表示两位数，不足两位数的用0表示
    quarter = '%02d' % (quarter * 3)

    date = '{}{}'.format(year, quarter)

    # 根据用户输入重新构造URL
    url = 'http://data.eastmoney.com/bbsj/{}/{}.html'.format(date, category)
    page = int(input('请输入要爬取的页码数：'))
    return url, page, category, date

class DownloadDataTable(object):
    def __init__(self, url, date, category, page=10):
        self.url = url
        self.page = page
        self.date = date
        self.category = category
        # self.browser = webdriver.Chrome()
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--headless')
        self.browser = webdriver.Chrome(chrome_options=self.chrome_options)
        self.wait = WebDriverWait(self.browser, 10)

    def get_index(self, page):
        """爬取页面"""
        try:
            self.browser.get(self.url)
            print('正在爬取第 %d 页' % page)
            self.wait.until(EC.presence_of_element_located((By.ID, 'dt_1')))
            if page > 1:
                page_input = self.wait.until(EC.presence_of_element_located((By.ID, 'PageContgopage')))
                page_input.click()
                page_input.clear()
                page_input.send_keys(page)
                submit = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.btn_link')))
                submit.click()
                time.sleep(5)
            self.wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#PageCont > span.at'), str(page)))
        except TimeoutException:
            print("页面爬取超时")

    def parse_index(self):
        """解析数据"""
        table_element = self.browser.find_element_by_css_selector('#dt_1')
        td_content = self.browser.find_elements_by_tag_name('td')
        tds = list()
        for td in td_content:
            tds.append(td.text)
        col = len(table_element.find_elements_by_css_selector('tr:nth-child(1) td'))
        tds = [tds[i: i+col] for i in range(0, len(tds), col)]
        list_link = list()
        links = table_element.find_elements_by_css_selector('#dt_1 a.red')
        for link in links:
            url = 'http://data.eastmoney.com' + link.get_attribute('href')
            list_link.append(url)
        list_link = pd.Series(list_link)
        df_table = pd.DataFrame(tds)
        df_table['url'] = list_link
        return df_table

    def write_to_csv(self, table):
        """存入表格"""
        if not os.path.exists('tables'):
            os.mkdir('tables')
        table.to_csv('tables/{}.csv'.format(self.category), mode='a', encoding='utf_8_sig', index=0, header=0)

    def run(self, page):
        try:
            self.get_index(page)
            df_table = self.parse_index()
            self.write_to_csv(df_table)
            print(print('%s页爬取成功' % page))
        except Exception:
            print('%s页爬取失败' % page)

    def main(self):
        for i in range(1, self.page + 1):
            # 爬取第二页和后面的页面时候，会在前一页的基础之上进行跳转，因此不能关闭浏览器，否则会报错
            self.run(i)
        self.browser.close()


if __name__ == '__main__':
    url, page, category, date = get_userdata()
    downloadpage = DownloadDataTable(url, date, category, page)
    downloadpage.main()