"""
爬取今日头条图片
完成版还存一个问题：就是爬取图片的时候，会提示403和502的错误
单独去爬取报错的图片没有问题，批量去爬取的时候就会报错，初步判断为反爬虫导致，目前无法解决，后续寻找新方法解决
"""
import requests
from urllib.parse import urlencode
import time
import os
from hashlib import md5
from multiprocessing.pool import Pool


headers = {
    'Host': 'www.toutiao.com',
    'Referer': 'https://www.toutiao.com/search/?keyword=%E7%8C%AB%E5%92%AA',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    'Cookie': 'tt_webid=6828751722031744525; s_v_web_id=verify_kaeqtdr1_wNrfoDfT_OdLP_4brU_9Mnq_vTWP7jrGRbzy; WEATHER_CITY=%E5%8C%97%E4%BA%AC; SLARDAR_WEB_ID=b1f16476-b888-4f40-9397-2998df13d771; tt_webid=6828751722031744525; csrftoken=db5a9009952404b5f1687f7566ce8c96; _ga=GA1.2.1978329278.1589942679; _gid=GA1.2.1130636522.1589942679; ttcid=70740dbea4164ad68b4f74a3ea2a598037; tt_scid=LQOlXhA1DE0X1wyYJendTk8m16TtA3kiBl4gY8ZFTH6eG98GtFANStadfiZahZaJ4c2c; __tasessionId=sznrki9us1589952031169'
}


def get_page(offset, keyword):
    """
    循环URL获取页面响应
    :param offset:  序号，0,20,40
    :param keyword: 搜索关键词
    :return: 响应内容
    """
    # 获取当前时间的时间戳，取整数部分
    timestamp = str(time.time()).split('.')[0]
    params = {
        'aid': '24',
        'app_name': 'web_search',
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'en_qc': '1',
        'cur_tab': '1',
        'from': 'search_tab',
        'timestamp': timestamp
    }
    url = 'https://www.toutiao.com/api/search/content/?' + urlencode(params)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError:
        print('Connection Filed!')
        return None


def get_images(json):
    """
    根据返回的json响应内容，找到图片的下载链接
    :param json:
    :return:
    """
    if json.get('data'):
        for item in json.get('data'):
            images_list = list()
            # 数据中会扦插一些广告数据，需要排除
            if item.get('image_list'):
                # 标题中会有一些特殊字符串，需要替换，否则创建目录的时候，会把这个“/”当做一级目录
                title = item.get('title').replace('/', '')
                images = item.get('image_list')
                for image in images:
                    images_list.append(image.get('url'))
                yield {'title': title, 'image': images_list}


def save_image(images):
    """
    根据返回的图片列表，保存数据，并根据图片名称的MD5值进行去重
    :param images:
    :return:
    """
    # 因为图片是不同的网站，所以需要单独构建headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
        'Host': 'p3-tt.byteimg.com',
        'Cookie': 'tt_webid=6828751722031744525; s_v_web_id=verify_kaeqtdr1_wNrfoDfT_OdLP_4brU_9Mnq_vTWP7jrGRbzy; WEATHER_CITY=%E5%8C%97%E4%BA%AC; SLARDAR_WEB_ID=b1f16476-b888-4f40-9397-2998df13d771; tt_webid=6828751722031744525; csrftoken=db5a9009952404b5f1687f7566ce8c96; _ga=GA1.2.1978329278.1589942679; _gid=GA1.2.1130636522.1589942679; ttcid=70740dbea4164ad68b4f74a3ea2a598037; tt_scid=l.H4gWjKC.IVsKXhQi89zAVa6hOQ0TG0FvBWXxJc1UlAY0eP.SZFalVM0BRlBVzS4779',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    # 根据标题创建目录
    image_path = os.path.join('image', images.get('title'))
    # 判断目录是否存在
    if not os.path.exists(image_path):
        os.mkdir(image_path)
    for image in images.get('image'):
        # 循环遍历图片链接列表中的每个列表
        try:
            reponse = requests.get(image, headers=headers)
            if reponse.status_code == 200:
                # 使用md5计算值，进行图片去重
                # 因为路径的名称中会包含特殊字符，不采用format的格式化
                # md5加密数据，返回md5 hash类型的值，其之接受byte字节流类型的数据做参数
                # hexdigest将计算出来的hash值转换成十六进制的数据
                img_path = '%s/%s.%s' % (image_path, md5(reponse.content).hexdigest(), 'jpg')
                # 不存在该路径，则会新图片，保存
                if not os.path.exists(img_path):
                    with open(img_path, 'wb') as f:
                        f.write(reponse.content)
                else:
                    print('Already Downloaded', img_path)
        except Exception as err:
            print(err)


def main(offset, keyword):
    json = get_page(offset, keyword)
    for item in get_images(json):
        print(item)
        save_image(item)


if __name__ == '__main__':
    # 定义offset循环列表
    GROUP_START = 0
    GROUP_END = 5
    groups = [x * 20 for x in range(GROUP_START, GROUP_END)]
    keyword = '猫咪'
    # 创建进程池
    pool = Pool()
    for offset in groups:
        pool.apply_async(main, (offset, keyword))
    pool.close()
    pool.join()