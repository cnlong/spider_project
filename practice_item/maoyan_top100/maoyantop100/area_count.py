# 数据处理
import pandas as pd
# pyplot和pylab都是绘制函数图的工具，但是pylab更为全面，包含了许多NumPy和pyplot中的函数，能够进行计算和绘图
import matplotlib.pyplot as plt
import pylab as pl  # 用于修改x轴坐标


# 设置绘图风格，默认的不好看
plt.style.use('ggplot')
# 设置图片大小
fig = plt.figure(figsize=(8, 5))
# 定义图表title、text标注的颜色
color1 = '#6D6D6D'
# 设置pd读取csv文件时候给定的列标题，也就是表头
columns = ['index', 'thumb', 'name', 'star', 'area', 'time', 'score']
# header，原文件没有表头，设置header为None,并通过names手动指定表头
#index_col设置索引为Index，不设置，默认索引 为0 1 2 3 。。。
# 使用pd读取文件
df = pd.read_csv('maoyantop100.csv', encoding='utf-8',header=None, names=columns, index_col='index')
# 排序，按照得分进行降序排列
df_score = df.sort_values('score', ascending=False)

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# 上述步骤对数据进行处理，处理完成之后开始绘图
# 比较100部电影都来自哪些国家
# groupby按区域共同元素进行聚合,然后计算同区域下元素的数量，再从大到小进行排序
# 此时返回的新对象，是对原文件进行处理之后的文件，也就是聚合计算排序之后的新文件
# area
# --      44
# 美国      18
# 韩国       7
# 法国       7
# 意大利      7
# 日本       4
# ......
area_count = df.groupby(by='area').area.count().sort_values(ascending=False)
# 绘图，并设置图表颜色为深蓝色，直接使用新的排序文件进行绘图
area_count.plot.bar(color='#4652B1')
plt.savefig('area_count.jpg')

plt.bar(range(15), area_count.values, tick_label=area_count.index, color='#4652B1')
for x, y in enumerate(list(area_count.values)):
    plt.text(x, y+0.5, '%s' % round(y, 1), ha='center', color=color1)
plt.title('各国/地区电影数量排名', color=color1)
plt.xlabel('国家/地区')
plt.ylabel('数量（部）')
plt.tight_layout()
plt.savefig('area_count2.jpg')
