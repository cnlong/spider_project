import os
from wordcloud import WordCloud

d = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()
with open(os.path.join(d, 'legend1900.txt')) as f :
    text = f.read()
    # colormap色图种类可从matplotlib文档中寻找，不同种类，词云的颜色变化不同
    # https://matplotlib.org/examples/color/colormaps_reference.html
    wc = WordCloud(scale=2, max_font_size=100,background_color='#383838', colormap='Blues')
    wc.generate_from_text(text)
    wc.to_file('19002.jpg')