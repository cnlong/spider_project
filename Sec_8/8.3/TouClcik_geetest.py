import requests
from hashlib import md5
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from PIL import Image
from io import BytesIO
import time


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


class TouClickGeetest(object):
    """极验验证码后台点触验证码破解"""
    def __init__(self):
        self.url = 'https://auth.geetest.com/login'
        self.browser = webdriver.Chrome()
        self.email = 'test@test.com'
        self.password = 'test123'
        self.wait = WebDriverWait(self.browser, 20)

    def open(self):
        """打开登录后台，输入邮箱和密码"""
        self.browser.get(self.url)
        inputs = self.browser.find_elements_by_css_selector('.card .ivu-form-item .ivu-input')
        for i in inputs:
            if i.get_attribute('placeholder') == '请输入邮箱':
                email = i
                email.send_keys(self.email)
            else:
                password = i
                password.send_keys(self.password)

    def check_code(self):
        """获取验证按钮，点击验证"""
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_radar_tip')))
        button.click()

    def get_code_img(self):
        """获取点触验证码的标签元素"""
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_item_img')))
        return img

    def get_img_content(self, img):
        """获取图片内容"""
        src = img.get_attribute('src')
        img_content = requests.get(src).content
        return img_content

    def get_scale(self, img, img_content):
        """获取验证码原图和其在浏览器中的大小比例
           个人觉得这一步有点多余
        """
        # 获取图片的字节流数据（即二进制内容）
        # 然后写入内存
        f = BytesIO()
        f.write(img_content)
        img0 = Image.open(f)
        scale = [img.size['width']/img0.size[0], img.size['height']/img0.size[1]]
        return scale

    def login_cjy(self, img_content):
        """登录超级鹰，并上传图片内容"""
        cjy = Chaojiying_Client('xiaoyuer', 'cal09160829', '905619')
        result = cjy.PostPic(img_content, '9005')
        return result

    def analyse_result(self, result):
        """根据超级鹰的返回结果数据，提取点触验证码上的小图标的坐标"""
        print(result)
        # {'err_no': 0, 'err_str': 'OK', 'pic_id': '3106611134373900005', 'pic_str': '213,117|99,62|274,259|217,233', 'md5': '6327fb04b97940352e7c32f3c5c902d1'}
        if result['err_no'] == 0:
            position = result['pic_str'].split('|')
            print(position)
            # ['213,117', '99,62', '274,259', '217,233']
            position = [[int(j) for j in i.split(',')] for i in position]
            print(position)
            # [[213, 117], [99, 62], [274, 259], [217, 233]]
            return position

    def click_icon(self, img, position):
        """根据返回坐标，点击图标"""
        for item in position:
            ActionChains(self.browser).move_to_element_with_offset(img, item[0], item[1]).click().perform()
            time.sleep(1)

    def click_commit(self):
        """验证码点击完成，点击确认提交"""
        commit_btn = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.geetest_commit_tip')))
        commit_btn.click()

    def run(self):
        """总步骤"""
        self.open()
        self.check_code()
        time.sleep(2)
        img = self.get_code_img()
        img_content = self.get_img_content(img)
        result = self.login_cjy(img_content)
        position = self.analyse_result(result)
        self.click_icon(img, position)
        self.click_commit()


if __name__ == '__main__':
    geetestclick = TouClickGeetest()
    geetestclick.run()