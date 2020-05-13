import csv

with open('data2.csv', 'r', encoding='utf-8') as f:
    # 常见读对象
    reader = csv.reader(f)
    # 读取出来的对象返回是csv对象格式，需要遍历读取里面的内容
    for i in reader:
        print(i)