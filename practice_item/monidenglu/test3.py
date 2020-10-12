from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)

browser.get('https://www.itjuzi.com/login')
username = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="手机号/邮箱"]')))
password = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="密码"]')))
username.send_keys(input('用户名：'))
password.send_keys(input('密码：'))
submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.el-button--primary')))
submit.click()
time.sleep(20)
browser.get('https://www.itjuzi.com/investevent')
print(browser.page_source)