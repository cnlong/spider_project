import os
import numpy as np
from matplotlib.image import imread
from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator
from PIL import Image
import random


def grey_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    """定义改变颜色的功能函数"""
    # 随机设置hsl色值
    return "hsl(0, 0%%, %d%%)" % random.randint(50, 100)


def wc_english(file_name):
    d = os.path.dirname(__file__) if '__file__' in locals() else os.getcwd()
    with open(os.path.join(d, file_name)) as f:
        text = f.read()
        # 读取背景图片
        # 将图片转换成像素点数组矩阵
        # background_image = np.array(Image.open(os.path.join(d, 'mask1900.jpg')))
        background_image = imread(os.path.join(d, 'mask1900.jpg'))
        # 从转换后的数组矩阵中提取背景图片颜色
        img_colors = ImageColorGenerator(background_image)
        # 设置屏蔽英文词
        stopwords = set(STOPWORDS)
        # 自定义添加需要屏蔽的单词
        stopwords.add('one')
        wc = WordCloud(
            margin=2,
            # 以读取的背景图片作为词云的形状
            mask=background_image,
            scale=2,
            min_font_size=4,
            max_words=200,
            stopwords=stopwords,
            random_state=42,
            background_color='black',
            max_font_size=150,
            # color_func=grey_color_func
        )
        wc.generate_from_text(text)
        # 根据图片底色设置字体颜色
        # 不设置字体颜色的时候，以默认的方式显示
        # wc.recolor(color_func=img_colors)
        # 根据新的变色函数来设置字体的颜色
        # wc.recolor(color_func=grey_color_func)
        wc.to_file('1900pro.jpg')


wc_english('legend1900.txt')