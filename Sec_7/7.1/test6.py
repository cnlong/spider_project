from selenium import webdriver
import time

browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
# 查找搜索框
input = browser.find_element_by_id('q')
# 输入查找内容
input.send_keys('iPhone')
time.sleep(2)
# 清除查找内容
input.clear()
input.send_keys('iPad')
# 查找搜索框提交按钮
button = browser.find_element_by_class_name('btn-search')
# 触发点击动作完成搜索
button.click()
time.sleep(5)
browser.close()