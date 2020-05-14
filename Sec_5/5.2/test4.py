"""改进插入数据的方法，无需修改插入方法，只需更改插入数据即可"""
import pymysql

data = {
    'id': '20120003',
    'name':'haha',
    'age': 20
}

table = 'student'
keys = ','.join(data.keys())
# 构造values后面的(%s, %s, %s)
# 根据数据长度，构造一个含有"%s"的数组，怎么就能组合成%s, %s, %s
values = ','.join(['%s'] * len(data))
sql = 'INSERT INTO {table} ({keys}) values ({values})'.format(table=table, keys=keys, values=values)
db = pymysql.connect(host='192.168.6.160', user='root', password='123456', port=3306, db='spiders')
cursor = db.cursor()
try:
    cursor.execute(sql, tuple(data.values()))
    print('susscessful')
    db.commit()
except Exception as err:
    print(err)
    db.rollback()
db.close()
