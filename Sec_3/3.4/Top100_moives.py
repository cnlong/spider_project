import requests
import re
import json


# 抓取第一页的信息
# 定义一个方法
# 注意猫眼的反爬机制，需要登录验证，目前通过设置cookie跳过验证，但是过期之后还需要重新验证
def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
        'Cookie': '__mta=213833643.1588818566648.1588818964035.1588819112559.11; uuid_n_v=v1; uuid=8F160880900A11EA9F54C3F723D2036BF5CB9F5D651847488C74A1C00E35F57D; _csrf=1fa943e94972f5829efc685f3d4c5f7a800465180b5b803ef0e96f457097f488; t_lxid=171ecf75cf9c8-0570d0dc612262-3c3f5a0c-15f900-171ecf75cf9c8-tid; _lxsdk=8F160880900A11EA9F54C3F723D2036BF5CB9F5D651847488C74A1C00E35F57D; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1588818567; mojo-uuid=41fcc792e68782a44a1e6a33daaaa99b; mojo-session-id={"id":"b2a269b996bab34a11f15148d53bb540","time":1588818566616}; __mta=213833643.1588818566648.1588818571653.1588818578968.3; mojo-trace-id=18; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1588819112; _lxsdk_s=171ecf75cfa-1e-7b4-87f%7C%7C27'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None


# 定义页面解析方法
def parse_one_page(html):
    # 创建正则规则对象
    pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>', re.S)
    # 匹配
    items = re.findall(pattern, html)
    for i in items:
        yield {
            'index': i[0],
            'image': i[1],
            'title': i[2].strip(),
            'actor': i[3].strip(),
            'time': i[4].strip(),
            'socre': i[5]+i[6]
        }


# 写入文件
def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        # 指定ensure_ascii=False，保证输出结果是中文新式，而不是unicode编码，并添加换行符
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(offset):
    # url添加偏移量
    url = "https://maoyan.com/board/4?offset={0}".format(offset)
    html = get_one_page(url)
    # print(html)
    movies = parse_one_page(html)
    for i in movies:
        write_to_file(i)


if __name__ == '__main__':
    # 遍历10次
    for i in range(10):
        main(offset=i * 10)