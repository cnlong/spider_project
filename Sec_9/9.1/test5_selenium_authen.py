"""
使用带用户密码的认证代理，较为繁琐
注意：下列代理无需用户密码认证，仅为测试
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import zipfile

ip = '113.101.151.171'
port = 4216
username = 'foo'
password = 'bar'

# 设置两个js文件来生成代理的密码认证文件，保存当前的认证用户名密码。较为繁琐
manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ]
    "background": {
        "script": ["background.js"]
    }
}
"""

background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
            singleProxy: {
                scheme: "http",
                host: "%(ip)s",
                port: "%(port)s"    
            }
        }
    }
    
chrome.proxy.settings.set({value: config, scope: "regular"}, function(){});
function callbackFn(details) {
    return {
        authCredentials: {
            username: "%(username)s",
            password: "%(password)s"
        }
    }
}
chrom.webRequest.onAuthRequired.addListener(
    callbackFn,
    {urls: ["<all_urls>"]},
    ['blocking']
)
""" % {'ip': ip, 'port': port, 'username': username, 'password': password}
plugin_file = 'proxy_auth_plugi.zip'
with zipfile.ZipFile(plugin_file, 'w') as zp:
    zp.writestr("manifest.json", manifest_json)
    zp.writestr("background.js", background_js)
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_extension(plugin_file)
browser = webdriver.Chrome(options=chrome_options)
browser.get('http://httpbin.org/get')
