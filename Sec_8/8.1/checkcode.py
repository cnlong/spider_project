"""
https://my.cnki.net/Register/CommonRegister.aspx
中国知网图像验证码破解
"""
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from PIL import Image
from io import BytesIO
import pytesseract

class CheckCodeCnki(object):
    """中国知网图形验证码"""
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.url = 'https://my.cnki.net/Register/CommonRegister.aspx'

    def open(self):
        self.browser.get(self.url)
        username = self.browser.find_element_by_id('username')
        password = self.browser.find_element_by_id('txtPassword')
        email = self.browser.find_element_by_id('txtEmail')
        return username, password, email

    def get_check_code(self):
        check_code = self.browser.find_element_by_id('checkcode')
        size = check_code.size
        location = check_code.location
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        check_code_img = screenshot.crop((left, top, right, bottom))
        return check_code_img

    def get_code_number(self, check_code_img):
        image = check_code_img.convert('L')
        threshold = 127
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)

        image = image.point(table, '1')
        result = pytesseract.image_to_string(image)
        return result

    def run(self):
        username, password, email = self.open()
        checkcode = self.browser.find_element_by_id('txtOldCheckCode')
        code_img = self.get_check_code()
        result = self.get_code_number(code_img)
        username.send_keys('lkhgvajs')
        password.send_keys('CKH1Y75KJ')
        email.send_keys('271138425@qq.com')
        checkcode.send_keys(result)
        self.browser.find_element_by_id('ButtonRegister').click()


if __name__ == '__main__':
    cnkicode = CheckCodeCnki()
    cnkicode.run()


