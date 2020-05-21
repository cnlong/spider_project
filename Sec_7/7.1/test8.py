from selenium import webdriver
import time

browser = webdriver.Chrome()
browser.get('https://www.zhihu.com/explore')
# execute_script执行JavaScript动作，也就是JS中编写使用的语言
# 进度条从上拉倒最底部
browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
# 弹出alert提示框
browser.execute_script('alert("To Bottom")')
