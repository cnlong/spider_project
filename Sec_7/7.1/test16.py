import time
from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.baidu.com')
# 执行JavaScript打开一个新的选项卡
browser.execute_script('window.open()')
# 获取当前开启的所有选项卡
print(browser.window_handles)
# 根据索引切换到新的选项卡中
browser.switch_to.window(browser.window_handles[1])
browser.get('https://www.taobao.com')
time.sleep(3)
browser.switch_to.window(browser.window_handles[0])
browser.get('https://www.jd.com')
time.sleep(2)
# 只会关闭当前打开的浏览器窗口
browser.close()
print(browser.window_handles)
# 目前程序在的窗口是上一次被删除的窗口（虽然浏览器显示是在新的浏览器），仍需要切回到新的浏览器
browser.switch_to.window(browser.window_handles[0])
browser.close()
