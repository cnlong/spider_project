from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

browser = webdriver.Chrome()
url = 'https://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'
browser.get(url)
# 根据iframe的id切换
browser.switch_to.frame('iframeResult')
try:
    logo = browser.find_element_by_class_name('logo')
except NoSuchElementException:
    print("Not Founf Logo!")
# 切换会父级frame
browser.switch_to.parent_frame()
logo = browser.find_element_by_class_name('logo')
print(logo)
print(logo.text)
browser.close()