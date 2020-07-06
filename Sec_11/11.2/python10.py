import pymongo

client = pymongo.MongoClient('192.168.6.160')
db = client['igetget']
collection = db['books']

with open('books.txt', 'r') as f:
    books = eval(f.read())
    for book in books:
        data = {
            'title': book.get('title'),
            'cover': book.get('index_img'),
            'summary': book.get('intro'),
            'price': book.get('cost_intro').get('price')
        }
        collection.insert_one(data)