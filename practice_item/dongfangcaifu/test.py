from selenium import webdriver

browser = webdriver.Chrome()
browser.get('http://data.eastmoney.com/bbsj/202006/lrb.html')
# 根据html标签的id定位表格标签
element = browser.find_element_by_css_selector('#dt_1')
# 找出表格中的所有td节点
td_content = element.find_elements_by_tag_name('td')
tds = []
for td in td_content:
    tds.append(td.text)
print(tds)
browser.close()

