from redis import StrictRedis

redis = StrictRedis(host='192.168.6.160', port=6379, db=0)
redis.set('name', 'Bob')
print(redis.get('name'))
print(redis.exists('name'))
print(redis.type('name'))
print(redis.keys('n*'))
print(redis.dbsize())

print(redis.getset('name', 'Mike'))
print(redis.get('name'))
print(redis.mget(['name', 'get']))

print(redis.rpush('list1', 1, 2, 3))
print(redis.lrange('list1', 1, 3))

print(redis.sadd('tags', 'Book', 'Tes', 'Coffee'))
print(redis.sunion('tags'))

print(redis.zadd('grade', 100, 'Bob', 98, 'Mike'))
print(redis.zadd('grade', 96, 'liming'))
print(redis.zrange('grade', 0, 3))

print(redis.hset('price', 'cake', '5'))
print(redis.hget('price', 'cake'))
