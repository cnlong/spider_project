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
# 从文件的time一列中提取年份时间，保存至读取对象中
df['year'] = df['time'].map(lambda x: x.split('-')[0])

# 查看文件大致信息
# print(df.info())
# 按年进行聚合，然后计算同一年电影的总数，并排序
grouped_year = df.groupby('year')
grouped_year_amount = grouped_year.year.count()
top_year = grouped_year_amount.sort_values(ascending=False)


# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# 上述步骤对数据进行处理，处理完成之后开始绘图
top_year.plot.bar(color='orangered')
for x, y in enumerate(list(top_year.values)):
    plt.text(x, y+0.1, '%s' % round(y, 1), ha='center', color=color1)
plt.title('电影数量年份排名', color=color1)
plt.xlabel('年份（年）')
plt.ylabel('数量（部）')
plt.tight_layout()

plt.savefig('film_year.jpg')