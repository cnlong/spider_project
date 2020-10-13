import os
from wordcloud import WordCloud
from matplotlib import pyplot as plt

# __file__显示当前文件的路径
# locals()返回当前位置的全部局部变量的字典
# 判断局部变量中是否包含“__file__”，如果包含，则获取os.path.dirname(__file__)的值赋予给d
# 如果不包含“__file__”变量，则将os.getcwd()的返回值赋予给d
# 获取当前文件的目录
d = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()
with open(os.path.join(d, 'legend1900.txt')) as f :
    text = f.read()
    # 生成词云对象，画布放大两倍，其中最大字号为100
    wc = WordCloud(scale=2, max_font_size=100)
    # 向词云中加载文字内容
    wc.generate_from_text(text)
    # 将词云保存为文件
    wc.to_file('1900.jpg')