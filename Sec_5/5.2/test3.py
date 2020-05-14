import pymysql

id = '20120002'
user = 'Bob'
age = 20

db = pymysql.connect(host='192.168.6.160', user='root', password='123456', port=3306, db='spiders')
cursor = db.cursor()
sql = 'INSERT INTO student (id, name, age) VALUES (%s, %s, %s)'
try:
    cursor.execute(sql, (id, user, age))
    # 插入数据后，需要提交事务
    db.commit()
except Exception as e :
    print(e)
    # 插入失败，回滚事务
    db.rollback()
db.close()