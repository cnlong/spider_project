from selenium import webdriver
from selenium.webdriver import ActionChains

brower = webdriver.Chrome()
url = 'https://www.zhihu.com/explore'
brower.get(url)
logo = brower.find_element_by_id('zh-top-link-logo')
print(logo)
print(logo.get_attribute('class'))