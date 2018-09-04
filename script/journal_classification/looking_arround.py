from pymongo import MongoClient
from functools import reduce
import pandas as pd

MONGO_URI = 'mongodb://localhost:27017'
MONGO_DATABASE = 'col-scienti-dev'
MONGO_COLLECTION = 'groups'


if __name__ == '__main__':
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DATABASE]
    groups_colletion = db[MONGO_COLLECTION]

    query = {
    "products.category": "Artículos publicados"
    }
    projection = {
        "products.issn": 1,
        "_id": 1
    }
    groups = groups_colletion.find(query, projection)
    total_products = reduce((lambda acum, cur: acum + len(cur['products'])), groups.__copy__(), 0)
    print('Total products to search:', total_products)

    filename = "scimagojr 2017.csv"
    df = pd.read_csv(filename, sep=';', index_col=0, low_memory=False)
    df['Issn'] = df['Issn'].apply(str)
    output_df = pd.DataFrame(columns=['issn', 'quartile'])
    missing_count = 0
    found_count = 0
    visited_count = 0
    for group_data in groups:
        for product in group_data['products']:
            visited_count += 1
            if visited_count % 8000 == 1:
                percentage = (visited_count * 100) / total_products
                print('{:0.3f}%% of products scanned'.format(percentage))
                print('Missing issns so far:', missing_count)
                print('Found issns so far:', found_count)
            try:
                issn = str(product['issn'])
                query_issn = issn.replace('-', '')
                t = df[df['Issn'].str.contains(query_issn)]
                if not t.empty:
                    found_count += 1
                    values = t[['Title', 'SJR Best Quartile']]
                    values_as_dict = {
                        'issn': query_issn,
                        'quartile': values[0][1]
                    }
                    output_df.append(values_as_dict)
                else:
                    missing_count += 1
            except KeyError:
                pass
    output_df.to_csv('output.csv')
    print('\r\rFinal results')
    print('Total missing issns', missing_count)
    print('Total found issns', found_count)
# Missing issns so far: 132379
# Found issns so far: 95195
# Traceback (most recent call last):
#   File "looking_arround.py", line 33, in <module>
#     for group_data in groups:
#   File "/home/cluster/Repos/grupvis/script/env/lib/python3.5/site-packages/pymongo/cursor.py", line 1189, in next
#     if len(self.__data) or self._refresh():
#   File "/home/cluster/Repos/grupvis/script/env/lib/python3.5/site-packages/pymongo/cursor.py", line 1126, in _refresh
#     self.__send_message(g)
#   File "/home/cluster/Repos/grupvis/script/env/lib/python3.5/site-packages/pymongo/cursor.py", line 982, in __send_message
#     helpers._check_command_response(first)
#   File "/home/cluster/Repos/grupvis/script/env/lib/python3.5/site-packages/pymongo/helpers.py", line 152, in _check_command_response
#     raise CursorNotFound(errmsg, code, response)
# pymongo.errors.CursorNotFound: cursor id 28193038900 not found
