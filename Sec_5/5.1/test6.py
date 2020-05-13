import csv

# newline=''参数，控制新文件中每行不会间隔一个空行
with open('data2.csv', 'w', newline='') as f:
    fieldnames = ['id', 'name', 'age']
    # 构建写对象，传入头部
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    # 写入头部数据
    writer.writeheader()
    writer.writerow({'id': '10001', 'name': 'Mike', 'age': 20})
    writer.writerow({'id': '10002', 'name': 'Bob', 'age': 21})
    writer.writerow({'id': '10003', 'name': 'Jordan', 'age': 22})