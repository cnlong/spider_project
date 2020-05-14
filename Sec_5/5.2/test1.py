import pymysql

# 连接数据库
db = pymysql.connect(host='192.168.6.160', user='root', password='123456', port=3306)
# 创建数据库游标对象
cursor = db.cursor()
# 查询数据库版本信息
cursor.execute('SELECT VERSION()')
# 因为上一条命令执行的是查询语句，需要调用相关方法获取查询的结果
data = cursor.fetchone()
print('Database version:', data)
cursor.execute("CREATE DATABASE spiders DEFAULT  CHARACTER SET utf8")
# 关闭连接
cursor.close()
db.close()
