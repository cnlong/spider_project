"""改进插入数据的方法，无需修改插入方法，只需更改插入数据即可"""
import pymysql

data = {
    'id': '20120003',
    'name':'haha',
    'age': 30
}

table = 'student'
keys = ','.join(data.keys())
values = ','.join(['%s'] * len(data))
# 插入语句
sql = 'INSERT INTO {table} ({keys}) values ({values}) ON DUPLICATE KEY UPDATE'.format(table=table, keys=keys, values=values)
# 更新语句
update = ','.join([" {key}=%s".format(key=key) for key in data])
# 合并语句
sql += update
db = pymysql.connect(host='192.168.6.160', user='root', password='123456', port=3306, db='spiders')
cursor = db.cursor()
try:
    cursor.execute(sql, tuple(data.values())*2)
    print('susscessful')
    db.commit()
except Exception as err:
    print(err)
    db.rollback()
db.close()
