import csv
from collections import namedtuple

# with open('stocks.csv') as f:
#     f_csv = csv.reader(f)
#     print(type(f_csv))
#     for i in f_csv:
#         print(i)

def get_data(file_name):
    with open(file_name) as f:
        f_csv = csv.reader(f)
        headings = next(f_csv)
        Row = namedtuple('Row', headings)
        for i in f_csv:
            print(Row(*i))

# for i in get_data('stocks.csv'):
#     print(i)
Row = namedtuple('Row', ['name', 'age', 'city'])
print(Row(*['xiaowang', '18', 'nanjing']))
print(Row(*['xiaoli', '18', 'nanjing']))
