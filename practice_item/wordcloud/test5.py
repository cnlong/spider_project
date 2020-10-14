import jieba
import wordcloud
from wordcloud import WordCloud,ImageColorGenerator
from matplotlib.image import imread


def cut_words(file_name):
    """使用jieba 对文本进行精确分词"""
    with open(file_name, encoding='utf-8') as f:
        text = f.read()
        # cut_all=False，表示精确模式进行分词
        # 返回的是一个生成器对象，包含分词的文本
        text = jieba.cut(text, cut_all=False)
        # 将分词之后的对象组成新的文本对象，每个单词之间以空格划分
        content = ''
        for i in text:
            content += i
            content += ' '
        return content


def get_stopwords(file_name):
    """获取stopwords词库中的单词"""
    with open(file_name, encoding='utf-8') as f:
        stopwords = list()
        for line in f.readlines():
            stopwords.append(line.strip())
    return stopwords


def move_stopwords(content, stopwords):
    """根据stopwords词库生成的列表，逐一删除分词后文本中的stopwords"""
    new_content = ''
    for word in content:
        if word not in stopwords:
            # 去除掉文本中的换行符和制表符
            if word != '\t' and '\n:':
                new_content += word
    # 缩减文本中的空格
    new_content = new_content.replace('   ', ' ').replace('  ', ' ')
    # 将新生成的文本保存至文件中
    with open('new_content.txt', 'w',encoding='utf-8') as f:
        f.write(new_content)
    return new_content


def get_wordcloud(new_content, image_name):
    """生成词云"""
    # 设置中文字体，中文必须设置字体否则会出错
    font_path = 'C:\Windows\Fonts\simhei.ttf'
    # 读取背景图片。转化为数组矩阵
    backgroud_image = imread(image_name)
    # 提取图片背景颜色
    img_color = ImageColorGenerator(backgroud_image)
    # 创建词云
    wc = WordCloud(
        font_path=font_path, # 中文字体
        margin=2,
        mask=backgroud_image,
        scale=2,
        max_words=200,
        min_font_size=4,
        random_state=42,
        background_color='white',
        max_font_size=100,
        color_func=img_color
    )
    wc.generate(new_content)
    wc.to_file('lc.jpg')


if __name__ == '__main__':
    content = cut_words('langchao2.txt')
    stopwords = get_stopwords('stopwords_cn.txt')
    new_content = move_stopwords(content, stopwords)
    get_wordcloud(new_content, 'mask1900.jpg')