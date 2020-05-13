import csv

with open('data.csv', 'w') as f:
    # 创建csv写对象
    writer = csv.writer(f, delimiter=' ')
    # 写入一行记录
    writer.writerow(['id', 'name', 'age'])
    writer.writerow(['10001', 'Mike', '20'])
    writer.writerow(['10002', 'Bob', '22'])
    writer.writerow(['10003', 'Jordan', '21'])