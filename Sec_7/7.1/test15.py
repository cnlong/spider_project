from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.zhihu.com/explore')
# 获取所有所有的Cookies，也可以根据cookie的名字获取单个cookie
print(browser.get_cookies())
# 通过字典传入额外的cookie
browser.add_cookie({'name': 'name', 'domain': 'www.zhihu.com', 'value': 'germy'})
print(browser.get_cookies())
# 删除所有cookies
browser.delete_all_cookies()
print(browser.get_cookies())
browser.close()