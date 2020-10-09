import csv
import json
import requests


def set_url():
    """根据用户输入参数，构造URL"""
    input_category = int(input('请选择查询的报表类型：'
                         '1.业绩报表，'
                         '2.业绩快报，'
                         '3.业绩预告，'
                         '4.预约披露时间，'
                         '5.资产负债表'
                         '6.利润表'
                         '7.现金流量表：'))
    category_dict = {
        1: ['RPT_LICO_FN_CPD', 'NOTICE_DATE,SECURITY_CODE'],
        2: ['RPT_FCI_PERFORMANCEE', 'UPDATE_DATE,SECURITY_CODE'],
        3: ['RPT_PUBLIC_OP_PREDICT', 'NOTICE_DATE,SECURITY_CODE'],
        4: ['RPT_PUBLIC_BS_APPOIN', 'FIRST_APPOINT_DATE,SECURITY_CODE'],
        5: ['RPT_DMSK_FN_BALANCE', 'NOTICE_DATE,SECURITY_CODE'],
        6: ['RPT_DMSK_FN_INCOME', 'NOTICE_DATE,SECURITY_CODE'],
        7: ['RPT_DMSK_FN_CASHFLOW', 'NOTICE_DATE,SECURITY_CODE']
    }
    category = category_dict[input_category]
    year = int(input('请输入查询年份（2009-2020）：'))
    quater = int(input('请选择查询季报类型：'
                       '1.第一季季报，'
                       '2.年中报，'
                       '3.第三季度，'
                       '4.年报：'))
    date_dict = {
        1: '03-31',
        2: '06-30',
        3: '09-30',
        4: '12-31'
    }
    date = date_dict[quater]
    date = str(year) + '-' + date
    page = int(input('请输入查询的页数：'))
    return category, date, page


def get_table_data(page, category, date):
    """爬取页面获取数据"""
    filter = '(REPORT_DATE=%27{}%27)'.format(date)
    type = category[0]
    if type == 'RPT_LICO_FN_CPD' or type == 'RPT_PUBLIC_OP_PREDICT':
        filter = '(REPORTDATE=%27{}%27)'.format(date)
    st = category[1]
    params = {
        'type': type,
        'sty': 'ALL',
        'p': page,
        'ps': 50,
    }
    url = 'http://datacenter.eastmoney.com/api/data/get?&{}&{}&{}'.format('sr=-1,-1',
                                                                       'filter={}'.format(filter),
                                                                          'st={}'.format(st))
    response = requests.get(url, params=params).text
    # print(requests.get(url, params=params).url)
    content = json.loads(response)['result']['data']
    return content


def writer_header(category, content):
    filepath = 'tables/{}.csv'.format(category[0])
    headers = list(content[0].keys())
    with open(filepath, 'a', newline='') as f:
        writer = csv.DictWriter(f, headers)
        writer.writeheader()


def writer_row(category, content):
    filepath = 'tables/{}.csv'.format(category[0])
    for data in content:
        with open(filepath, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data.values())


def main():
    category, date, page = set_url()
    for i in range(1, page+1):
        content = get_table_data(i, category, date)
        if i == 1:
            writer_header(category, content)
        writer_row(category, content)


if __name__ == '__main__':
    main()