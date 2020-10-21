import pymongo

client = pymongo.MongoClient('192.168.6.160')
print(client.list_database_names())
db = client.huxiu
print(db)