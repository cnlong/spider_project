import json

data = [{
    'name': '王伟',
    'gender': '男',
    'birthday': '1992-10-18'
}]

# 指定保存数据的编码，保存中文
with open('data2.json', 'w', encoding='utf-8') as f:
    # indent保存为JSON格式的数据
    # ensure_ascii=False，输出中文
    f.write(json.dumps(data, indent=2, ensure_ascii=False))