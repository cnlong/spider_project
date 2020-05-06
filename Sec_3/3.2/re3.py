import re
content = "http://weibo.com/comment/kEraCN"
# 结尾非贪婪，尽可能少的匹配字符，这个时候只会匹配一个空字符
res1 = re.match("http.*?comment/(.*?)", content)
# 结尾贪婪，尽可能多的匹配字符，会匹配所有符合要求的字符
res2 = re.match("http.*?comment/(.*)", content)

print("re1:", res1.group(1))
print("re2:", res2.group(1))