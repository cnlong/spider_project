import requests
import json

headers = {
      "Referer":"https://m.weibo.cn/u/2830678474?sudaref=cuiqingcai.com&display=0&retcode=6102",
      "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
      "X-Requested-With":"XMLHttpRequest",
      "X-XSRF-TOKEN":"609539"
  }

url = "https://m.weibo.cn/api/container/getIndex?sudaref=cuiqingcai.com&display=0&retcode=6102&type=uid&value=2830678474&containerid=1076032830678474"
while True:
 response = requests.get(url,headers=headers)
 try:
     since_id = json.loads(response.content)["data"]["cardlistInfo"]["since_id"]
     print(since_id)
 except:
     break
 url = "https://m.weibo.cn/api/container/getIndex?sudaref=cuiqingcai.com&display=0&retcode=6102&type=uid&value=2830678474&containerid=1076032830678474&since_id=" + str(since_id)
 content = json.loads(response.content)["data"]["cards"]
 # for i in range(10):
 #     try:
 #         print(content[i]["mblog"]["text"])
 #     except:
 #         continue