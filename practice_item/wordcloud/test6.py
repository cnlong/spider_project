import requests
from requests import RequestException
import pandas as pd
from bs4 import BeautifulSoup
from wordcloud import WordCloud


def get_page():
    """获取页面中前500学校的表格"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
    }
    url = 'https://www.dxsbb.com/news/2619.html'
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # 中文网址响应返回会乱码，对返回内容通过RFC标准编码进行编码，然后进行解码即可
            return response.text.encode('ISO-8859-1').decode('gbk')
    except RequestException:
        print('爬取失败')


def get_table(html):
    """解析表格"""
    soup = BeautifulSoup(html, 'lxml')
    content = soup.select('table')[0]
    tb = pd.read_html(content.prettify(), header=0)[0]
    tb.rename(columns={'排名': 'word_rank', '学校名称': 'university', '国家/地区': 'country'}, inplace=True)
    # index=None，去除默认的索引存入csv
    tb.to_csv('university.csv', mode='a', encoding='utf_8_sig', index=None)
    return tb


def get_dataframe(tb):
    """将获取的表格按照国家继续分组，并获的新的数据"""
    # 根据国家进行分组，并计算数量
    # 注意这一步返回的数据样式，并不是正常的格式，如下述格式，还需重新排序，方便绘制
    #          word_rank  university
    # country
    # 中国              26          26
    # 中国台湾            12          12
    # 中国澳门             1           1
    # 中国香港             6           6
    # 丹麦               5           5
    # ...            ...         ...
    df = tb.groupby(by='country').count()
    # 对分组后的数据按照新表格的“word_rank”进行重新排序，行降序排序得到新的series数据
    # 这里的“word_rank”不是表格初始的1-500的排序，而是对其进行计算后得到新的“word_rank”即计算后的数量值
    df = df['word_rank'].sort_values(ascending=False)
    return df


def get_wordcloud(df):
    font_path = 'C:\Windows\Fonts\simhei.ttf'
    wc = WordCloud(
        font_path=font_path,  # 中文字体
        margin=2,
        scale=2,
        max_words=200,
        min_font_size=4,
        random_state=42,
        background_color='white',
        max_font_size=100,
        colormap='viridis'
    )
    wc.generate_from_frequencies(df)
    wc.to_file('uni.jpg')


if __name__ == '__main__':
    html = get_page()
    tb = get_table(html)
    df = get_dataframe(tb)
    get_wordcloud(df)