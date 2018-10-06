from pymongo import MongoClient
import pandas as pd
from progress.bar import Bar
from functools import reduce
import logging

logger = logging.getLogger(__name__)

MONGO_URI = 'mongodb://localhost:27017'
MONGO_DATABASE = 'col-scienti-dev'
MONGO_COLLECTION = 'groups'

VALID_PRODUCT_TYPES = [
    'Artículos publicados', 'Libros publicados',
    'Capítulos de libro publicados'
]


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

    query = {"institution": "Universidad Tecnológica De Pereira - Utp"}
    projection = {
        'code': 1,
        'knowledgeArea': 1,
        'universityName': 1,
        'classification': 1,
        'products': 1,
        'groupName': 1,
        'gruplacURL': 1
    }

    groups_result = groups_collection.find(query, projection)
    total_products_to_scan = reduce(
        lambda acum, group: acum + len(group['products']),
        groups_result.__copy__(), 0)
    total_products = 0
    total_valid_products = 0
    valid_products = []

    bar = Bar('Processing', max=total_products_to_scan)
    for group in groups_result:
        for product in group['products']:
            if product['category'].strip() in VALID_PRODUCT_TYPES:
                total_valid_products += 1
                product_data = {
                    # 'university': get_and_clean(group, 'institution'),
                    'groupCode': get_and_clean(group, 'code'),
                    'groupName': get_and_clean(group, 'groupName'),
                    'groupKnowledgeArea': get_and_clean(
                        group, 'knowledgeArea'),
                    'groupClassification': get_and_clean(
                        group, 'classification'),
                    'productType': get_and_clean(product, 'category'),
                    'productTitle': get_and_clean(product, 'title'),
                    'productYear': get_and_clean(product, 'year'),
                    'approved': get_and_clean(product, 'isApproved')
                }
                if not product_data['productTitle']:
                    logging.error(
                        '\nFollowing product has not name: %s.\nGroup link: %s',
                        product, group['gruplacURL'])
                valid_products.append(product_data)
            total_products += 1
            bar.next()
    bar.finish()
    columns = [
        'university', 'groupCode', 'groupName', 'groupKnowledgeArea',
        'groupClassification', 'productType', 'productTitle', 'productYear',
        'approved'
    ]
    report_df = pd.DataFrame(valid_products, columns=columns)
    report_df.to_csv('products_resport.csv', index=False)

    logging.info(f'Total scanned products: {total_products}')
    logging.info(f'Total valid products: {total_valid_products}')
