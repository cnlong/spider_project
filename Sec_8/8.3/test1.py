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


class Chaojiying_Client(object):
    """超级鹰官方API文档"""
    def __init__(self, username, password, soft_id):
        self.username = username
        self.password = md5(password.encode('utf8')).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()

url = 'https://auth.geetest.com/login/'
EMAIL = 'test'
PASSWORD = 'test'
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 20)
browser.get(url)
inputs = browser.find_elements_by_css_selector('.card .ivu-form-item .ivu-input')
for i in inputs:
    if i.get_attribute('placeholder') == '请输入邮箱':
        email = i
    else:
        password = i
email.send_keys(EMAIL)
password.send_keys(PASSWORD)

button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_radar_tip')))
button.click()

time.sleep(3)

# 注意，这里想要获取验证码的图片及验证的小图标，不能采取截图的方式，因为截取到的是在页面中显示的图片，
# 而不是真正包含两者的图片
# img = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_item_img')))
# if not img:
#     raise SystemExit('Not fonud img')
# location = img.location
# size = img.size
# top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width']
# scrennshot = browser.get_screenshot_as_png()
# scrennshot = Image.open(BytesIO(scrennshot))
#
# img_captcha = scrennshot.crop((left, top, right, bottom))
# img_captcha.save('img_caprcha.png')

img = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_item_img')))
src = img.get_attribute('src')
# 获取图片的二进制内容
img_content = requests.get(src).content
f = BytesIO()
f.write(img_content)
# 将图片以文件的形式打开，主要是为了获取图片的大小
img0 = Image.open(f)
print(img0)
# 获取图片与浏览器该标签大小的 比例
scale = [img.size['width']/img0.size[0], img.size['height']/img0.size[1]]
# 登录超级鹰平台
cjy = Chaojiying_Client('xiaoyuer', 'cal09160829', '905619')
# 9005是其平台对应的验证码类型
# 获取图片字节流的数据，传入超级鹰平台
result = cjy.PostPic(img_content, '9005')
# 分析结果
# 错误结果为0，即为分析正常
if result['err_no'] == 0:
    position = result['pic_str'].split('|')
    print(position)
    position = [[int(j) for j in i.split(',')] for i in position]
    print(position)

    # 模拟点击
    for items in position:
        # 根据图片比例，以及返回坐标，计算准确坐标位置
        ActionChains(browser).move_to_element_with_offset(img, items[0]*scale[0], items[1]*scale[1]).click().perform()
        time.sleep(1)

commit_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.geetest_commit_tip')))
commit_btn.click()