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

# 上述步骤对数据进行处理，处理完成之后开始绘图
# 取出排序后数据的前10者的name作为绘图的x轴
# 取出排序后数据的前10者的score作为绘图的y轴
name1 = df_score.name[:10]
score1 = df_score.score[:10]

# 绘制图表
# range(10)使用序列作为x轴的位置序列，便于x轴的正确排序，因为x轴一般是以名字显示，所以很难使用名字进行x轴排序
# 索引x轴序列，先使用range，然后在用名字替换即可
# 得分作为y轴的序列，y轴都是数字，可以直接直接作为序列，会以y轴的序列规律生成图标的y轴
# tick_label作为x轴每个序列的名称
plt.bar(range(10), score1, tick_label=name1)
# 设置纵坐标轴的范围
plt.ylim((9, 9.8))
# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# 设置图表的标题和其颜色
plt.title('电影评分最高 Top10', color=color1)
# 设置x轴标题
plt.xlabel('电影名称')
# 设置y轴标题
plt.ylabel('评分')
# 为图表中每个条形图添加数值标签，也就是x,y轴的位置添加文本内容
# plt.text(x, y, s),x即x轴，y即y轴，s即文本内容
# enumerate能够将一个列表转换成枚举对象，类似于键为索引，值为元素的字典
# round函数返回浮点数的四舍五入值，可以决定小位数有几位
for x, y in enumerate(list(score1)):
    plt.text(x, y+0.01, '%s' % round(y, 1), horizontalalignment='center', color=color1)

# x轴名称太长，多个名称之间会重叠，将名称旋转为纵向显示
plt.xticks(rotation=270)
# 自动控制空白边缘，以全部显示x轴名称，避免只显示部分
plt.tight_layout()
plt.savefig('top10.jpg')