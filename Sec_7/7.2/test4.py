import requests
from urllib.parse import quote

# 定制JavaScript脚本
lua = """
function main(splash)
    return 'hello'
end
"""
# 转码lua脚本成URL编码，通过lua_source参数传递
url = 'http://192.168.6.160:8050/execute?lua_source=' + quote(lua)
response = requests.get(url)
print(response.text)