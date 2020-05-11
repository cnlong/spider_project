from pyquery import PyQuery as pq

doc = pq(filename='test.html')
print(doc('li'))