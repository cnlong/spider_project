from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
# 在内存中读写Bytes数据
from io import BytesIO
from PIL import Image
import requests
import cv2
from selenium.webdriver import ActionChains


def get_track(distance):
    """
    根据偏移量获取移动轨迹
    :param distance:偏移量
    :return:移动轨迹
    """
    # 移动轨迹
    track = []
    # 当前位移
    current = 0
    # 减速阈值
    mid = distance * 4 / 5
    # 计算间隔
    t = 0.2
    # 初速度
    v = 0

    while current < distance:
        if current < mid:
            # 加速度为正2
            a = 2
        else:
            # 加速度为负3
            a = -3
        # 初速度v0
        v0 = v
        # 当前速度v = v0 + at
        v = v0 + a * t
        # 移动距离x = v0t + 1/2 * a * t^2
        move = v0 * t + 1 / 2 * a * t * t
        # 当前位移
        current += move
        # 加入轨迹
        track.append(round(move))
    return track

# 定义登录极验需要的用户名和密码
USERNAME = '1840191734@qq.com'
PASSWORD = 'cal09160829'

# 1.访问网站
url = 'https://qzone.qq.com/'
browser =  webdriver.Chrome()
# browser = webdriver.Firefox()
# browser.maximize_window()
wait = WebDriverWait(browser, 10)
browser.get(url)

# 注意这里存在子frame，需要切换到子frame
browser.switch_to.frame('login_frame')

# 获取切换账户密码登录按钮
browser.find_element_by_id('switcher_plogin').click()

# 获取账户和密码框
browser.find_element_by_id("u").send_keys(USERNAME)
browser.find_element_by_id("p").send_keys(PASSWORD)

# 点击登录
browser.find_element_by_id('login_button').click()
time.sleep(3)

# 切换到滑动验证码的frame中
browser.switch_to.frame("tcaptcha_iframe")

# 选择拖动滑块的节点
slide_element = browser.find_element_by_id('tcaptcha_drag_thumb')
# 获取滑块图片的节点
slideBlock_ele = browser.find_element_by_id('slideBlock')
slideBlock_img_url = slideBlock_ele.get_attribute('src')
responsebk = requests.get(slideBlock_img_url)
with open('slideBlock.jpg', 'wb') as f:
    f.write(responsebk.content)
# 获取缺口背景图片节点
slideBg = browser.find_element_by_id('slideBg')
slideBg_img_url = slideBg.get_attribute('src')
responsebg = requests.get(slideBg_img_url)
with open('slidebg.jpg', 'wb') as f:
    f.write(responsebg.content)

# 二值化有缺口的图片
target_rgb = cv2.imread('slidebg.jpg')
target_gray = cv2.cvtColor(target_rgb, cv2.COLOR_BGR2GRAY)
template_rgb = cv2.imread('slideBlock.jpg', 0)
res = cv2.matchTemplate(target_gray, template_rgb, cv2.TM_CCOEFF_NORMED)
value = cv2.minMaxLoc(res)
value = value[3][0]
track = get_track(value)
time.sleep(3)

ActionChains(browser).click_and_hold(browser.find_element_by_id('tcaptcha_drag_thumb')).perform()
for x in track:
    ActionChains(browser).move_by_offset(xoffset=x, yoffset=0).perform()
time.sleep(0.5)
ActionChains(browser).release().perform()