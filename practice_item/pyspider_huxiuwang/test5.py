"""数据清洗"""
import pymongo
import pandas as pd


client = pymongo.MongoClient('192.168.6.160')
db = client['huxiu']
collection = db['huxiu_new']
# 将数据库数据转换成dataframe
df = pd.DataFrame(list(collection.find()))
# 查看行数和列数
print(df.shape)
# 查看总体情况
print(df.info())
# 输出前5行
print(df.head())
# 删除无用的_id列
df.drop(['_id'], axis=1, inplace=True)
# 将name中的特殊字符替换为空
df['author'].replace('©', '', inplace=True, regex=True)
# 将字符更改为数值,ignore，无效的解析将返回输入
df = df.apply(pd.to_numeric, errors='ignore')
# 为了方便，将write_time列中，包含几分钟、小时、天前的行，全部替换为今天的时间
df['write_time'] = df['write_time'].replace('.*前', '2020-10-26', regex=True)
# 将时间转为时间格式对象
df['write_time'] = pd.to_datetime(df['write_time'])
# 判断是否有数据重复，False不重复
print(any(df.duplicated()))
# # 提取重复值数量
# print(df.duplicated().value_counts())
# # 删除重复值
# df = df.drop_duplicates(keep='first')
# # 删除部分行后，会导致Index中断，重新设置Index
# df = df.reset_index(drop=True)
# 增加两列数据，一列是文章标题长度列，一列是年份列
df['title_length'] = df['title'].apply(len)
df['month'] = df['write_time'].dt.month
print(df.info())