import requests
url = 'http://cms-bucket.ws.126.net/2020/0907/79a345dcj00qga3ip012xc0015o04yxc.jpg?imageView&thumbnail=550x0'
response = requests.get(url)
# 图片的内容是二进制保存的
with open('四川省.jpg', 'wb') as f:
    f.write(response.content)