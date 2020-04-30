import requests
import re


headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
}

r = requests.get('https://www.zhihu.com/explore', headers=headers)
# 指定匹配规则
# re.S表示匹配扩展“.”的匹配范围，包括匹配换行符“\n”
pattern = re.compile('<.*?"ExploreSpecialCard-contentTitle".*?>(.*?)</a>', re.S)
title = re.findall(pattern, r.text)
print(title)