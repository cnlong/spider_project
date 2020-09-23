"""
采用数据API接口去爬取数据，避免Selenium的前端交互，导致爬取速度过慢且占内存
"""
import requests
import json
import csv


def get_table_data(i):
    params = {
        'type': 'RPT_DMSK_FN_INCOME',
        'sty': 'ALL',
        'p': i,
        'ps': 50,
        'st': 'NOTICE_DATE,SECURITY_CODE',
        # 传入Url的参数会自动转码，对于特殊字符的参数，会导致URL不正确，所以这两个参数暂时不通过参数传入
        # 'sr': '-1,-1',
        # 'filter': '(REPORT_DATE=%272020-06-30%27)'
    }

    url = 'http://datacenter.eastmoney.com/api/data/get?&{}&{}'.format('sr=-1,-1', 'filter=(REPORT_DATE=%272020-06-30%27)')
    response = requests.get(url, params=params).text
    content = json.loads(response)['result']['data']
    return content


def writer_header(content):
    headers = list(content[0].keys())
    file_path = 'tables/{}.csv'.format('test')
    with open(file_path, 'a', encoding='utf_8_sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()


def writer_row(content):
    file_path = 'tables/{}.csv'.format('test')
    for data in content:
        with open(file_path, 'a', encoding='utf_8_sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data.values())


for page in range(1, 11):
    content = get_table_data(page)
    if page == 1:
        writer_header(content)
    writer_row(content)
