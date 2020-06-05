"""
登录存在问题就是，获取到了用户名输入框，但是无法交互，目前无法解决
"""
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from PIL import Image
from io import BytesIO
from selenium.webdriver import ActionChains

USERNAME = '13809023772'
PASSWORD = 'xxxxxxxxxx'

class CrackWeiBo(object):
    def __init__(self):
        self.url = 'https://passport.weibo.cn/signin/login'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        self.username = USERNAME
        self.password = PASSWORD

    def open(self):
        self.browser.get(self.url)
        username = self.wait.until(EC.presence_of_element_located((By.ID, 'loginName')))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'loginPassword')))
        submit = self.wait.until(EC.presence_of_element_located((By.ID, 'loginAction')))
        print(username.get_attribute('placeholder'))
        username.send_keys(self.username)
        password.send_keys(self.password)
        submit.click()

    def position(self):
        """获取验证码位置"""
        try:
            img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'patt-shadow')))
        except TimeoutException:
            print("未出现验证码")
            self.open()
        time.sleep(2)
        location = img.location
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width']
        return (top, bottom, left, right)

    def get_screenshot(self):
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_image(self, name='captcha.png'):
        top, bottom, left, right = self.position()
        screenshot = self.position()
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save(name)
        return captcha

    def main(self):
        count = 0
        while True:
            self.open()
            self.get_image(str(count)+'.png')
            count += 1


if __name__ == '__main__':
    crack = CrackWeiBo()
    crack.main()

