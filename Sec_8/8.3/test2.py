from hashlib import md5
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from PIL import Image
from io import BytesIO
import time
import requests
import pytesseract

browser = webdriver.Chrome()
url = 'https://my.cnki.net/Register/CommonRegister.aspx'
wait = WebDriverWait(browser, 20)
browser.get(url)
username = browser.find_element_by_id('username')
password = browser.find_element_by_id('txtPassword')
email = browser.find_element_by_id('txtEmail')
img = wait.until(EC.presence_of_element_located((By.ID, 'checkcode')))
size = img.size
print(size)
location = img.location
print(location)
screenshot = browser.get_screenshot_as_png()
screenshot = Image.open(BytesIO(screenshot))
top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width']
print("验证码位置", top, bottom, left, right)
image = screenshot.crop((left, top, right, bottom))
# image.save('code.png')
# # src = img.get_attribute('src')
# # img_content = requests.get(src).content
# f = BytesIO()
# f.write(img_content)
# image = Image.open(f)
image = image.convert('L')
# 设定阈值
threshold = 127
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)

image = image.point(table, '1')
result = pytesseract.image_to_string(image)
print(result)

username.send_keys('xiaozhayu')
password.send_keys('CKH@123%^&')
email.send_keys('271138425@qq.com')
checkcode = browser.find_element_by_id('txtOldCheckCode')
checkcode.send_keys(result)
browser.find_element_by_id('ButtonRegister').click()
