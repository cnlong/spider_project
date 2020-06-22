"""
注意github首页的动态信息，是通过ajax加载获取的
直接从首页的请求response中是获取不到的，需要访问ajax中的请求地址才能获取动态信息
"""
import requests
from pyquery import PyQuery as pq


class Login(object):
    """Login类"""
    def __init__(self):
        self.headers = {
            'Referer': 'https://github.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
            'Host': 'github.com'
        }
        # 登录url
        self.login_url = 'https://github.com/login'
        # 登录请求的url
        self.post_url = 'https://github.com/session'
        # github个人信息页url
        self.logined_url = 'https://github.com/settings/profile'
        # 动态信息由ajax请求的，在首页的返回结果中找不到，需要请求新的Url
        self.feed_url = 'https://github.com/dashboard-feed'
        # session请求，保持长连接，一个会话处理多个请求，共享cookies
        self.session = requests.session()

    def token(self):
        """从登录页源码中获取token"""
        # 发送请求
        response = self.session.get(self.login_url, headers=self.headers)
        # 解析请求返回源码,构建Xpath对象
        selector = pq(response.text)
        # 匹配源码中的token
        # 注意lxml找到的结果都是以列表形式返回的
        token = selector('input[name="authenticity_token"]').attr('value')
        return token

    def login(self, email, password):
        """登录"""
        # 定义登录表单提交的数据
        data = {
            'commit': 'Sign in',
            'authenticity_token': self.token(),
            'login': email,
            'password': password
        }
        # 发送登录post请求
        response = self.session.post(self.post_url, data=data, headers=self.headers)
        # 访问ajax请求获取动态信息
        response = self.session.get(self.feed_url, headers=self.headers)
        if response.status_code == 200:
            self.dynamics(response.text)
        # 发送个人详情页请求
        response = self.session.get(self.logined_url, headers=self.headers)
        if response.status_code == 200:
            self.profile(response.text)

    def dynamics(self, html):
        """获取首页所有用户的动态信息"""
        selector = pq(html)
        # 找出所有的动态信息元素
        dynamics = selector('div[class="d-flex flex-column width-full"] div[class="d-flex flex-items-baseline"] div').items()
        # # 遍历每条动态信息，提取文本内容
        for item in dynamics:
            dynamic = item.text().strip()
            print(dynamic)

    def profile(self, html):
        """个人详情页处理"""
        seclector = pq(html)
        # 获取个人信息页展示的用户名
        name = seclector('input[id="user_profile_name"]').attr('value')
        # 获取个人信息页展示的邮箱地址
        email = seclector('select[id="user_profile_email"] option[selected="selected"]').attr('value')
        print(name, email)


if __name__ == '__main__':
    login = Login()
    login.login(email='271138425@qq.com', password='xxxxxxxx')