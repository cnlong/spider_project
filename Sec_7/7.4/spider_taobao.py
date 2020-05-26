"""
注意，爬取第一步，需要登录淘宝，否则无法进入搜索页
解决办法：
1.手机扫码直接登录
2.编写模拟登录的代码
"""
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from  selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote

browser = webdriver.Chrome()
# 定义延时对象，超时则抛出异常
wait = WebDriverWait(browser, 20)
KEYWAORD = 'iPad'


def get_product():
    """
    根据浏览器访问页面的源码，获取商品信息
    :return:
    """
    pass


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
        print("Successfully!")
        browser.close()
    # 获取超时异常，重新爬取
    except TimeoutException:
        index_page(page)


if __name__ == '__main__':
    index_page(10)