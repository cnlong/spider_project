from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
# 设定10秒的等待时长对象
wait = WebDriverWait(browser, 10)
# 调用until方法，传入等待条件（也就是要查找的节点）
# presence_of_element_located代表节点出现的意思
# 10秒内加载出节点并返回，超时抛出异常
input = wait.until(EC.presence_of_element_located((By.ID, 'q')))
# element_to_be_clickable代表节点可点击，查找到节点，并在10秒内可点击，就返回这个节点，超时不可点击，则报错
button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-search')))
print(input, button)
browser.close()