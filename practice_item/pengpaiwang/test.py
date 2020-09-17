import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import os
import re
from urllib.parse import urlencode
from pyquery import PyQuery as pq
from multiprocessing import Pool

class DownloadPage(object):
    """爬取澎湃网美数课新闻数据"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
    }
    url = 'https://www.thepaper.cn/load_index.jsp?'

    def get_page_index(self, page):
        """爬取单个页面，获取页面的响应内容"""
        paras = {
            'nodeids': 25635,
            'pageidx': page
        }
        url = self.url + urlencode(paras)
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.text
        except RequestException:
            print("请求失败")
            return None

    def parse_page_index(self, html):
        """解析页面，获取每条新闻的标题及新闻的详情连接
        每条新闻的详情连接类似于https://www.thepaper.cn/newsDetail_forward_8558789
        后面的信息在每个新闻源码中
        """
        doc = pq(html)
        # 获取所有新闻
        data = doc('div > h2 > a')
        data_list = list(data.items())
        # 遍历获取每个新闻的标题及url
        for i in range(len(data_list)):
            yield {
                'title': data_list[i].text(),
                'url': 'https://www.thepaper.cn/' + data_list[i].attr('href')
            }

    def get_news_detail(self, news):
        """获取每个新闻的详情页"""
        url = news.get('url')
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.text
        except RequestException:
            print('请求失败')
            return None

    def parse_news_detail(self, html):
        """解析每个详情页内容"""
        soup = BeautifulSoup(html, 'lxml')
        if not soup.h1:
            return None
        # 获取标题
        title = soup.h1.string
        # 去掉标题中非法字符
        title = re.sub('[\/:*?"<>|]', '-', title).strip()
        if not os.path.exists(title):
            os.mkdir(title)
        text_path = '{0}/{1}.{2}'.format(title, 'news', 'txt')
        if soup.find(attrs={'class': 'news_txt'}):
            with open(text_path, 'w', encoding='utf-8') as f:
                f.write(soup.find(attrs={'class': 'news_txt'}).text)
        # 以防新闻详情中没有图片
        if len(soup.find_all(attrs={'style':'width:600px;'})) > 0:
            # 获取所有的图片,返回的是一个bs4的集合类型
            items = soup.find_all(attrs={'style':'width:600px;'})
            for i in range(len(items)):
                # 获取每个图片的url地址
                pic = items[i].attrs['src']
                yield {
                    'title': title,
                    'pic': pic,
                    'num': i
                }

    def save_pic(self, pic):
        """下载图片"""
        if pic==None:
            return None
        title = pic.get('title')
        url = pic.get('pic')
        num = pic.get('num')

        if not os.path.exists(title):
            os.mkdir(title)
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                img_path = '{0}/{1}.{2}'.format(title, num, 'jpg')
                if not os.path.exists(img_path):
                    with open(img_path, 'wb') as f:
                        f.write(response.content)
                        print('文章{0}的第{1}张图片下载完成'.format(title, num))
                else:
                    print('文章{0}的第{1}张图片已经下载'.format(title, num))
        except RequestException:
            print('文章{0}的第{1}张图片已经下载'.format(title, num))

    def main(self, i):
        html = self.get_page_index(i)
        data_list = self.parse_page_index(html)
        for item in data_list:
            html = self.get_news_detail(item)
            data = self.parse_news_detail(html)
            for pic in data:
                self.save_pic(pic)

    def run(self):
        pool = Pool()
        pool.map(self.main, [i for i in range(1, 5)])
        pool.close()
        pool.join()


if __name__ == '__main__':
    pengpai = DownloadPage()
    pengpai.run()
