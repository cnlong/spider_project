from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

url = 'https://auth.geetest.com/login'
browser = webdriver.Chrome()
browser.get(url)
wait = WebDriverWait(browser, 20)
button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_radar_tip')))
print(button)
button.click()
