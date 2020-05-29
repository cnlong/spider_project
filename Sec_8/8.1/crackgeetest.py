from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
# 在内存中读写Bytes数据
from io import BytesIO
from PIL import Image

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

    def get_position(self):
        """
        获取滑块图片验证码的位置
        :return: 验证码位置元组
        """
        # 获取滑块图片
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_img')))
        time.sleep(2)
        # 获取图片的位置，返回的是左上角的的到x轴的距离和到y轴的距离（以网页顶部为y轴，左侧为x轴）
        location = img.location
        # 获取图片的大小，即宽高
        size = img.size
        # 通过图片的位置和宽高，获取整个图片的上下左右的距离
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width']
        return (top, bottom, left, right)

    def get_screenshot(self):
        """
        获取网页截图
        :return: 截图对象
        """
        # 获取网页截图
        screenshot = self.browser.get_screenshot_as_png()
        # BytesIO(screenshot)从内存中读取返回的byte类型的截图对象
        # 用图片打开对象
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_slider(self):
        """
        获取移动滑块的按钮
        :return: 返回该对象
        """
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))
        return slider

    def get_geetest_image(self, name="captcha.png"):
        """
        获取滑块验证码的图片
        :return: 图片对象
        """
        # 获取滑块图片整体位置
        top, bottom, left, right = self.get_position()
        print("滑块图片位置", top, bottom, left, right)
        # 获取网页截图
        screenshot = self.get_screenshot()
        # 按照滑块的位置，截取滑块图片,左，上，右，下
        captcha = screenshot.crop((left, top, right, bottom))
        # 保存图片
        captcha.save(name)
        return captcha

    def open(self):
        """打开网页"""
        # 最大化浏览器
        self.browser.maximize_window()
        self.browser.get(self.url)
        # 获取登录邮箱和密码输入框
        email = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.card .ivu-form-item .ivu-input')))
        password = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.card .ivu-form-item-error .ivu-input')))
        # 输入登录邮箱和登录密码
        email.send_keys(self.email)
        password.send_keys(self.password)

    def is_pixel_qural(self, image1, image2, x, y):
        """

        :param image1:
        :param image2:
        :param x:
        :param y:
        :return:
        """




if __name__ == '__main__':
    geetest = CrackGeetest()
    button = geetest.get_geetest_button()
    button.click()
