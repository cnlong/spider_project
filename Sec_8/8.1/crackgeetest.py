from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# 定义登录极验需要的用户名和密码
EMAIL = 'test@test.com'
PASSWORD = '123456'

class CrackGeetest():
    def __init__(self):
        """初始化配置信息"""
        self.url = 'https://auth.geetest.com/login'
        self.browser =  webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        self.email = EMAIL
        self.password = PASSWORD

    def get_geetest_button(self):
        """
        获取初始验证按钮
        :return:  按钮对象
        """
        # 显示等待获取能够点击的验证按钮
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_radar_tip')))
        return button


if __name__ == '__main__':
    geetest = CrackGeetest()
    button = geetest.get_geetest_button()
    button.click()
