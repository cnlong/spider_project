import requests
from urllib.parse import quote

lua = """
function main(splash, args)
    local treat = require("treat")
    local response = splash:http_get("http://httpbin.org/get")
        return {
            html = treat.as_string(response.body),
            url = response.url,
            status = response.status
        }
end
"""
url = 'http://192.168.6.160:8050/execute?lua_source=' + quote(lua)
response = requests.get(url)
print(response.text)