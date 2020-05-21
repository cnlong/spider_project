from selenium import webdriver

brower = webdriver.Chrome()
url = 'https://www.zhihu.com/explore'
brower.get(url)
input = brower.find_element_by_css_selector('.ExploreHomePage-ContentSection-header span')
print(input.size, input.tag_name, input.location)
brower.close()
