# from selenium import webdriver
# # 在内存中处理字节bytes
# from io import BytesIO
# from PIL import Image
#
# url = 'https://www.zhihu.com/explore'
# browser = webdriver.Chrome()
# # 浏览器最大化
# browser.maximize_window()
# browser.get(url)
# # 保存截图
# browser.save_screenshot('screenshot.png')
# # 返回字节流的图片数据
# image = browser.get_screenshot_as_png()
# image = Image.open(BytesIO(image))
# print(image)
# browser.close()

"""
https://auth.geetest.com/login
此网站测试太多，滑块验证码就变成点触验证码
需要加入点触验证码
"""

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

# 1.访问网站
url = 'https://auth.geetest.com/login'
# browser =  webdriver.Chrome()
browser = webdriver.Firefox()
browser.maximize_window()
wait = WebDriverWait(browser, 20)
browser.get(url)

# 2.输入登录邮箱和密码输入框
# email = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.card .ivu-form-item .ivu-input')))
# password = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.card .ivu-form-item-error .ivu-input')))
inputs = browser.find_elements_by_css_selector('.card .ivu-form-item .ivu-input')
for i in inputs:
    if i.get_attribute('placeholder') == '请输入邮箱':
        email = i
    else:
        password = i
email.send_keys(EMAIL)
password.send_keys(PASSWORD)

# 3.点击验证按钮
button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_radar_tip')))
button.click()

# 4.获取滑块验证码的位置
img = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_img')))
time.sleep(2)
# 获取图片的位置，返回的是左上角的的到x轴的距离和到y轴的距离（以网页顶部为y轴，左侧为x轴）
location = img.location
# 获取图片的大小，即宽高
size = img.size
# 通过图片的位置和宽高，获取整个图片的上下左右的距离
top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width']
position  = (top, bottom, left, right)
print(position)

# 5.获取网页截图
screenshot = browser.get_screenshot_as_png()
# BytesIO(screenshot)从内存中读取返回的byte类型的截图对象
# 用图片打开对象
screenshot = Image.open(BytesIO(screenshot))

# 6.获取滑块按钮
slider = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))

# # 7,通过滑块位置和网页截图，获取完整的滑块图片
# # 获取滑块图片整体位置
# top, bottom, left, right = position
# print("滑块图片位置", top, bottom, left, right)
# # 按照滑块的位置，截取滑块图片,左，上，右，下
# captcha = screenshot.crop((left, top, right, bottom))
# # 保存图片
# captcha.save("captcha.png")

canvas = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '.geetest_fullpage_click_box .geetest_canvas_slice')))
print(canvas.location)
print(canvas.size)

# browser.close()
