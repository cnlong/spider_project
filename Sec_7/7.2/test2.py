import requests
url = 'http://192.168.6.160:8050/render.png?url=https://www.jd.com&wait=5&width=1000&height=700'
response = requests.get(url)
with open('jd.png', 'wb') as f:
    f.write(response.content)