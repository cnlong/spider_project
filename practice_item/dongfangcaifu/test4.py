import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


browser = webdriver.Chrome()
# 10秒显示等待时间，以便网页表格加载完成
wait = WebDriverWait(browser, 10)


def index_page(page):
    try:
        browser.get('http://data.eastmoney.com/bbsj/202006/lrb.html')
        print('正在爬取第：%s 页' % page)
        # 等待页面中ID为dt_1的标签加载完成
        wait.until(EC.presence_of_element_located((By.ID, 'dt_1')))
        # 判断输入的Page是否为1，不为1的时候需要进行翻页动作
        if page > 1:
            # 获取页码输入框
            input_page = wait.until(EC.presence_of_element_located((By.ID, 'PageContgopage')))
            # 点击输入框
            input_page.click()
            # 清空输入框
            input_page.clear()
            # 输入页码
            input_page.send_keys(page)
            # 获取跳转按钮
            submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.btn_link')))
            # 点击跳转按钮
            submit.click()
            time.sleep(5)
        # 比较当前页面中的页码是否需页码参数一致，验证是否跳转完成，或者是否是第一页
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#PageCont > span.at'), str(page)))
    except TimeoutException:
        return None


if __name__ == '__main__':
    for page in range(1, 5):
        index_page(page)