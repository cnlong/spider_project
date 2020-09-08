import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

colums = ["index", "thumb", "name", "star", "area", "time", "score"]
dataframe = pd.read_csv("maoyantop100.csv", header=None, names=colums, index_col='index')
# 保存演员的列表
starlist = []
# 获取表格中演员的series数据
star_total = dataframe.star
# dataframe.star是数据表中的Series对象，通过str获取每一行数据的字符串,将字符串中的空格去掉
# 通过str获取每一行数据去掉空格之后的字符串，然后通过逗号分隔得到每一行演员的列表，添加到总列表中
for i in dataframe.star.str.replace(' ', '').str.split(','):
    starlist.extend(i)
# 通过set对演员总列表进行去重
starall = set(starlist)
# print(len(starlist))
# print(len(starall))
starall2 = Counter()
for star in starlist:
    starall2[star] += 1

# 找出前15的演员及其参演电影数量
starall3 = dict(starall2.most_common(15))

# 绘图
# 以名字为x轴，参演电影数量为y轴
x_star = list(starall3.keys())
y_star = list(starall3.values())
# 设置绘图风格，默认的不好看
plt.style.use('ggplot')
# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.bar(range(15), y_star, tick_label=x_star)
for x, y in enumerate(y_star):
    plt.text(x, y+0.1, '%s' % round(y, 1), ha='center')
# x轴名字旋转
plt.xticks(rotation=270)
plt.ylim((0, 10))
plt.title('演员电影作品数量排名')
plt.xlabel('演员')
plt.ylabel('数量（部）')
plt.tight_layout()
plt.savefig('topstar.jpg')

# 提取每部电影的1号演员和2号演员
# 将获得的star的series数据逐一放入到匿名函数中进行处理提取
dataframe['star1'] = dataframe['star'].map(lambda x: x.split(',')[0])
dataframe['star2'] = dataframe['star'].map(lambda x: x.split(',')[1])
# dataframe[(dataframe['star1'] == '张国荣')|(dataframe['star2'] == '张国荣')] 筛选出演员中包含张国荣的电影
# [['star','name']]只显示名字和演员列表
# reset_index重新设置索引
star_most = dataframe[(dataframe['star1'] == '张国荣') | (dataframe['star2'] == '张国荣')][['star','name']].reset_index('index')
print(star_most)
# print(dataframe[['star','name']])
print(dataframe[(dataframe['star1'] == '张国荣')][['star','name']])
print(dataframe[(dataframe['star2'] == '张国荣')][['star','name']])

