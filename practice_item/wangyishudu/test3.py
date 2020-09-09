import requests
from requests import RequestException
from pyquery import PyQuery as pq
import os

class DownloadImage(object):
    """下载网易数读页面图片"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
    }
    # url = 'http://data.163.com/20/0907/16/FLUEM8EP00019GOE.html'
    # url = 'http://data.163.com/20/0907/12/FLU1IHKS00019GOE.html'
    url = 'http://data.163.com/20/0901/12/FLEIV3V100019GOE.html'

    def get_page(self):
        """请求页面"""
        try:
            response = requests.get(self.url, headers=self.headers)
            if response.status_code == 200:
                return response.text
        except RequestException:
            print('网页请求失败')
            return None

    def parse_page(self, html):
        """解析页面"""
        data = pq(html)('p > img')
        data_list = list(data.items())
        title = pq(html)('h1').text()
        for i in range(len(data_list)):
            pic_url = data_list[i].attr['src']
            yield {
                'title': title,
                'pic_url': pic_url,
                'num': i
            }

    def save_pic(self, pic):
        """保存图片"""
        url = pic.get('pic_url')
        title = pic.get('title')
        num = pic.get('num')
        # 判断目录是否存在
        if not os.path.exists(title):
            os.mkdir(title)
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                file_path = '{0}\{1}.{2}'.format(title, num, 'jpg')
                if not os.path.exists(file_path):
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                        print('图片：%s 下载成功' % num)
                else:
                    print('图片：%s 已下载' % num)
        except Exception as e:
            print('图片下载失败')

    def main(self):
        html = self.get_page()
        data = self.parse_page(html)
        for pic in data:
            self.save_pic(pic)


if __name__ == '__main__':
    image = DownloadImage()
    image.main()