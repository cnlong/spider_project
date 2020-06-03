"""
B站滑块验证码
https://blog.csdn.net/weixin_45042620/article/details/105905106
因为移动轨迹的问题，滑块移动不是特别准确，还需要调整参数
"""
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from PIL import Image
from io import BytesIO
import time
import random
from selenium.webdriver import ActionChains

username = input('请输入用户名：')
password = input('请输入密码：')

class BiliGeetest():
    """类函数"""
    def __init__(self):
        self.url = 'https://passport.bilibili.com/login'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        self.username = username
        self.password = password

    def get_login_btn(self):
        """获取登录按钮"""
        login = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-login')))
        login.click()
        time.sleep(3)
        print("登录成功")

    def get_screenshot(self):
        """获取网页截图"""
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_c_background(self):
        """获取带缺口的图片元素"""
        c_background = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'canvas.geetest_canvas_bg.geetest_absolute')))
        return c_background

    def get_c_slice(self):
        """获取滑块的图片元素"""
        c_slice = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'canvas.geetest_canvas_slice.geetest_absolute')))
        return c_slice

    def get_c_full_bg(self):
        """获取完整的背景图片元素"""
        c_full_bg = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'canvas.geetest_canvas_fullbg.geetest_fade.geetest_absolute')))
        return c_full_bg

    def get_background_img(self):
        """截取带缺口的验证码图片"""
        c_background = self.get_c_background()
        c_slice = self.get_c_slice()
        self.browser.execute_script("arguments[0].style=arguments[1]", c_slice, "display: none")
        screenshot = self.get_screenshot()
        img_size = c_background.size
        location = c_background.location
        top, bottom, left, right = location['y'], location['y'] + img_size['height'], location['x'], location['x'] + \
                                   img_size['width']
        c_background_img = screenshot.crop((left, top, right, bottom))
        c_background_img.save('c_background_img.png')
        self.browser.execute_script("arguments[0].style=arguments[1]", c_slice, "display: block")
        return c_background_img

    def get_full_bg_img(self):
        """截取完整图片的验证码图片"""
        c_full_bg = self.get_c_full_bg()
        self.browser.execute_script("arguments[0].style=arguments[1]", c_full_bg, "display: block")
        screenshot = self.get_screenshot()
        img_size = c_full_bg.size
        location = c_full_bg.location
        top, bottom, left, right = location['y'], location['y'] + img_size['height'], location['x'], location['x'] + \
                                   img_size['width']
        c_full_bg_img = screenshot.crop((left, top, right, bottom))
        c_full_bg_img.save(' c_full_bg_img.png')
        self.browser.execute_script("arguments[0].style=arguments[1]", c_full_bg, "display: none")
        return c_full_bg_img

    def get_distance(self, image1, image2):
        """获取图片像素差异的距离"""
        threshold = 60
        for x in range(image1.size[0]):
            for y in range(image1.size[1]):
                image1_pixel = image1.load()[x, y]
                image2_pixel = image2.load()[x, y]
                if not(abs(image1_pixel[0] - image2_pixel[0]) < threshold and abs(image1_pixel[1] - image2_pixel[1]) < threshold and abs(image1_pixel[2] - image2_pixel[2]) < threshold):
                    distance = x
                    return distance

    def get_trace(self, distance):
        """获取移动轨迹"""
        trace = []
        v = 0
        mid = distance * 4/5
        current = 0
        while current < distance:
            if current < mid:
                a = 2
            else:
                a = -3
            t = random.randint(3, 6)/10
            v0 = v
            v = v0 + a * t
            move = v0 * t + 0.5 * a * t * t
            if current + move >= distance:
                move = distance - current
            current += move
            trace.append(round(move))
        return trace


    def get_slider_button(self):
        """获取滑块移动按钮"""
        slider = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.geetest_slider_button')))
        return slider

    def move_slier(self, slider, trace):
        """移动滑块"""
        ActionChains(self.browser).click_and_hold(slider).perform()
        for x in trace:
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
            time.sleep(0.02)
        ActionChains(self.browser).release().perform()

    def open(self):
        """打开网页"""
        self.browser.get(self.url)
        username = self.browser.find_element_by_id('login-username')
        password = self.browser.find_element_by_id('login-passwd')
        username.send_keys(self.username)
        password.send_keys(self.password)

    def run(self):
        """运行"""
        self.open()
        self.get_login_btn()
        image1 = self.get_background_img()
        image2 = self.get_full_bg_img()
        distance = self.get_distance(image1, image2)
        slider = self.get_slider_button()
        trace = self.get_trace(distance)
        self.move_slier(slider, trace)


if __name__ == '__main__':
    crack = BiliGeetest()
    crack.run()
