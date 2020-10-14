import wordcloud
from wordcloud import WordCloud


with open('langchao2.txt', encoding='utf-8') as f:
    text = f.read()
    wc = WordCloud()
    # 获取文本中的词排序,找出高频词中不需要显示在词云中的单词，然后将其加入到stopwords中
    process_word = WordCloud.process_text(wc, text)
    sort = sorted(process_word.items(), key=lambda e: e[1], reverse=True)
    print(sort[:50])
