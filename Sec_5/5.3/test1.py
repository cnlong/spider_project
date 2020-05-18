import pymongo

# client = pymongo.MongoClient(host='192.168.6.160', port=27017)
client = pymongo.MongoClient("mongodb://192.168.6.160:27017/")
db = client['test']
collection = db['students']
student1 = {
    "id": "20200101",
    "name": "Jordan",
    "age": "20",
    "gender": "male"
}
student2 = {
    "id": "20200102",
    "name": "Mike",
    "age": "21",
    "gender": "female"
}

student3 = {
    "id": "20200103",
    "name": "Kevin",
    "age": "20",
    "gender": "female"
}

student4 = {
    "id": "20200104",
    "name": "Harden",
    "age": "20",
    "gender": "male"
}
# result = collection.insert_many([student3, student4])
# print(result)
# print(result.inserted_ids)

result1 = collection.find_one({'name': 'Mike'})
# print(result1)
# print(type(result1))
myquery = {'age': '20'}
result2 = collection.find(myquery)
print(result2)
print(type(result2))

result3 = collection.find({'age': {'$gt': '20'}})
# print(result3)
for i in result3:
    print(i)

result4 = collection.find({'name': {'$regex': '^M.*'}})
for i in result4:
    print(i)

count = collection.find().count()
count1 = collection.count_documents({'age': '20'})
print(count1)

# pymongo.ASCENDING指定升序，pymongo.DESCENDING指定降序
result5 = collection.find().sort('age', pymongo.ASCENDING)
print([result['id'] for result in result5])

result6 = collection.find().skip(2)
print([result['id'] for result in result6])

result7 = collection.find().limit(3)
print([result['id'] for result in result7])

condition = {'name': 'Mike'}
student = collection.find_one(condition)
student['age'] = 90
result = collection.update(condition, student)
print(result)
print(student)

result8 = collection.remove({'name': 'Mike'})
print(result8)