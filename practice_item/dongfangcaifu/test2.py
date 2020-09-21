from selenium import webdriver
import pandas as pd

browser = webdriver.Chrome()
browser.get('http://data.eastmoney.com/bbsj/202006/lrb.html')
element = browser.find_element_by_css_selector('#dt_1')
td_content = element.find_elements_by_tag_name('td')
tds = list()
for td in td_content:
    tds.append(td.text)
# 定位首行td节点，并结算td的数量即为列数
col = len(element.find_elements_by_css_selector('tr:nth-child(1) td'))
# 根据列数，划分上一步中获取到列表
tds = [tds[i:i+col] for i in range(0, len(tds), col)]
# 提取表格数据中，表格内容为详细的URL地址
list_link = list()
# 找出所有的“详细”链接的元素
links = element.find_elements_by_css_selector('#dt_1 a.red')
for link in links:
    url = 'http://data.eastmoney.com' + link.get_attribute('href')
    list_link.append(url)

# 将单独提取出来的url列表转换成Pandas中的Series类型数据
list_link = pd.Series(list_link)
# 将按列数换分的列表转换成Pandas中的DataFrame类型数据
df_table = pd.DataFrame(tds)
# 将提取出来的url列添加到表格中,列名为url
df_table['url'] = list_link
# head()默认读取前五行数据
print(df_table.head())


browser.close()

