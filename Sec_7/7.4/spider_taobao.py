"""
注意，爬取第一步，需要登录淘宝，否则无法进入搜索页
解决办法：
1.手机扫码直接登录
2.编写模拟登录的代码
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from  selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
from pyquery import PyQuery as pq
import pymongo

# 使用无痕浏览器模式，无需打开网页
# 这里不能使用无痕浏览器模式，因为需要登录，无痕模式无法登录
# chrome_opitons = Options()
# chrome_opitons.add_argument('--headless')
# chrome_opitons.add_argument('--disable-gpu')
browser = webdriver.Chrome()
# 定义延时对象，超时则抛出异常
wait = WebDriverWait(browser, 20)
KEYWAORD = 'iPad'

# 定义MongoDB的相关信息
MONGO_HOST = '192.168.6.160'
MONGO_HOST_PORT = 27017
MONGO_DB = 'taobao'
MONGO_COLLECTION = 'products'
# 连接MongoDB
client = pymongo.MongoClient(host=MONGO_HOST, port=MONGO_HOST_PORT)
# 指定数据库
db = client[MONGO_DB]


def get_product(browser):
    """
    根据浏览器访问页面的源码，获取商品信息
    分析源码，因为大多数商品信息的源码都是一样的，所以分析一个，借此类推其他的的商品信息
    :return:
    """
    # 获取浏览器的源码
    html = browser.page_source
    # 使用pyquery解析源码
    doc = pq(html)
    # 根据CSS选择器选择所有商品信息的节点，注意返回的是PyQuery对象，需要使用其items方法转换成生成器，方便遍历
    items = doc('#mainsrp-itemlist .items .item').items()
    # 遍历获取每个商品节点的信息
    for item in items:
        # 遍历的每个单节点也是PyQuery对象，看使用pyquery方法查询其下的属性数据
        product = {
            # 找到图片节点，获取其地址属性
            # 图片这边有多个url地址，src是缩略图，data-src是大图
            'image': item.find('.pic .img').attr('data-src'),
            # 价格
            'price': item.find('.price').text(),
            # 购买人数
            'deal': item.find('.deal-cnt').text(),
            # 商品标题
            'title': item.find('.title').text(),
            # 店铺名称
            'shop': item.find('.shop').text(),
            # 地点
            'location': item.find('.location').text()
        }
        print(product)
        save_to_mongo(product)


def index_page(page):
    """
    根据页码索引获取指定页
    :param page: 页码
    :return:
    """
    print("正在爬取第", page, '页')
    try:
        # 根据搜索物品构建请求URL
        url = 'https://s.taobao.com/search?q=' + quote(KEYWAORD)
        browser.get(url)
        # 判断当前传入的页码，如果大于1，就跳转到指定页
        if page > 1:
            # 获取翻页的页码输入框
            # 10秒内加载出来该节点，就返回该节点元素，否则超时抛出异常
            # 根据CSS选择器选择该输入框
            input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))
            # 根据可点击条件及CSS选择器选择翻页中的确定提交按钮
            submit =wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit')))
            # 清除页码输入框原来的内容
            input.clear()
            # 传入指定的索引页码
            input.send_keys(page)
            # 点击提交按钮
            submit.click()
        # 跳转到指定的页码之后，下面翻页区域中的当前显示页会高亮显示，判断高亮显示的页码是否包含自己传入的Page
        # 包含，则程序继续运行，不包含，等待直至条件符合，超时抛出异常
        # 注意，这里比较的是字符串
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), str(page)))
        # 等待页面中的商品信息加载完成，超时抛出异常
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
        get_product(browser)
        # 不能主动关闭，否则会导致爬取第二页的时候报错invalid session id
        # browser.close()
    # 获取超时异常，重新爬取
    except TimeoutException:
        index_page(page)


def save_to_mongo(product):
    """
    保存数据到MongoDB
    :param product: 提取出来的商品相关数据
    :return:
    """
    try:
        if db[MONGO_COLLECTION].insert(product):
            print('存储到MongoDB成功')
    except Exception:
        print('存储到MongoDB失败')


if __name__ == '__main__':
    # 遍历前5页爬取数据
    max_page = 5
    for i in range(1, max_page+1):
        index_page(i)