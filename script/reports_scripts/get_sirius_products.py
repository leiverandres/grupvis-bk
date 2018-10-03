from pymongo import MongoClient
import pandas as pd
from progress.bar import Bar
from functools import reduce
import logging
from bson.json_util import dumps

logger = logging.getLogger(__name__)

MONGO_URI = 'mongodb://localhost:27017'
MONGO_DATABASE = 'col-scienti-dev'
MONGO_COLLECTION = 'groups'

SIRIUS_CODE = "COL0035995"


def connect_to_db():
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DATABASE]
    groups_collection = db[MONGO_COLLECTION]
    return groups_collection


def get_and_clean(object, key, default_val='Not found'):
    value = object.get(key, default_val)
    if type(value) is str:
        cleaned_val = value.strip().replace('\n', '').replace('\r', '')
        return cleaned_val
    return value


if __name__ == '__main__':
    groups_collection = connect_to_db()
    sirius = groups_collection.find_one({"code": SIRIUS_CODE})
    total_products = len(sirius['products'])
    bar = Bar('Processing products', max=total_products)
    processed_products = []
    import json
    json_data = dumps(sirius['products'])
    print(type(json_data))
    with open('sirius.json', 'w') as json_file:
        json.dump(json.loads(json_data), json_file)
    for product in sirius['products']:
        product_data = {
            'type': get_and_clean(product, 'category'),
            'subtype': get_and_clean(product, 'type'),
            'name': get_and_clean(product, 'title'),
            'year': get_and_clean(product, 'year', 'missing'),
            'approved': get_and_clean(product, 'isApproved')
        }
        processed_products.append(product_data)
        bar.next()
    bar.finish()
    columns = ['type', 'subtype', 'name', 'year', 'approved']
    report_df = pd.DataFrame(processed_products, columns=columns)
    report_df.to_csv('sirius_products_resport.csv')
    print('DONE')
