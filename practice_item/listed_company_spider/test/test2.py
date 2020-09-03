import requests
from requests import RequestException
import pandas as pd
from bs4 import BeautifulSoup
from lxml import etree
import time
import pymysql
# sqlalchemt是一个通过ORM操作数据库的框架
from sqlalchemy import create_engine
# 编码URL字符串
from urllib.parse import urlencode
import threading
import pymongo


# 程序起始时间
start_time = time.time()
print("开始时间: %s" % start_time)


def get_one_page(page, date):
    """
    页面爬取
    :param page: 爬取页码
    :param date:  Url传参之一，当前页面的爬取的日期时间
    :return: 爬取内容
    """
    # header头部
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
    }
    # url传参
    paras = {
        'reportTime': date,
        'pageNum': page
    }
    # 根据传参组建URL
    url = 'https://s.askci.com/stock/a/0-0?' + urlencode(paras)
    # 使用request爬取页面
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('爬取失败')


def parse_res(html):
    """
    解析爬取页面返回的响应内容
    :param html: 响应内容
    :return: 提取的数据
    """
    if html is None:
        return None
    # 创建解析对象
    soup = BeautifulSoup(html, 'html.parser')
    # 选出id为myTable04的元素块，也就是html中上市公司数据保存的元素块
    # 为了便于pd处理，一般提取出来的代码是表格元素块
    # 注意select返回的是list,list中保存的是bs4类型的HTML标签元素
    content = soup.select('#myTable04')[0]
    # prettify()优化HTML代码
    # read.html()返回的是list,从中取出DataFrame
    # 将html作为参数传给pd进行处理
    tbl = pd.read_html(content.prettify(), header=0)[0]
    # 重命名列名,将表格的列名更改为英文，方便存入数据库
    tbl.rename(columns = {'序号':'serial_number', '股票代码':'stock_code', '股票简称':'stock_abbre', '公司名称':'company_name', '省份':'province', '城市':'city', '主营业务收入(201812)':'main_bussiness_income', '净利润(201812)':'net_profit', '员工人数':'employees', '上市日期':'listing_date', '招股书':'zhaogushu', '公司财报':'financial_report', '行业分类':'industry_classification', '产品类型':'industry_type', '主营业务':'main_business'}, inplace=True)
    return tbl


def generate_mysql():
    """创建数据库表存放数据"""
    conn = pymysql.connect(
        host='192.168.6.246',
        user='root',
        password='123456',
        port=3306,
        charset='utf8',
        db='wade'
    )
    # 创建游标对象
    cursor = conn.cursor()
    # 创建数据表的sql语句
    sql = 'CREATE TABLE IF NOT EXISTS listed_company (serial_number INT(20) NOT NULL,stock_code INT(20) ,stock_abbre VARCHAR(20) ,company_name VARCHAR(20) ,province VARCHAR(20) ,city VARCHAR(20) ,main_bussiness_income VARCHAR(20) ,net_profit VARCHAR(20) ,employees VARCHAR(20) ,listing_date DATETIME(0) ,zhaogushu VARCHAR(20) ,financial_report VARCHAR(20) , industry_classification VARCHAR(20) ,industry_type VARCHAR(300) ,main_business VARCHAR(200) ,PRIMARY KEY (serial_number))'
    # 执行sql
    cursor.execute(sql)
    conn.close()


def write_to_sql(tbl, db='wade'):
    """使用ORM框架存数据到MySQL"""
    if tbl is None:
        return None
    # 创建数据库连接
    engine = create_engine('mysql+pymysql://root:123456@192.168.6.246:3306/{0}?charset=utf8'.format(db))
    # 写入数据
    # if_exists='append'表示在原有表基础之上增加
    try:
        tbl.to_sql('listed_company', con=engine, if_exists='append', index=False)
    except Exception as e:
        print(e)


def write_mongo(tbl):
    """插入MongoDB"""
    client = pymongo.MongoClient('192.168.6.160')
    db = client['wade']
    db['stock'].insert(tbl)


def run(page, date):
    """
    主函数
    :param page:
    :return:
    """
    # 爬取页面
    html = get_one_page(page, date)
    # 解析页面
    tbl = parse_res(html)
    # # 存入数据库
    # write_to_sql(tbl)
    write_mongo(tbl)

def main(page):
    # 创建数据表
    generate_mysql()
    # 注意这里的时间，会显示在数据表的表头中，所以需要保持一致
    date = '2018-12-31'
    for i in range(1, page):
       t1 = threading.Thread(target=run, args=(i, date))
       t1.start()


if __name__ == '__main__':
    main(180)
    print("耗时: %s" % (time.time() - start_time))



