from pymongo import MongoClient
import pandas as pd


def get_and_clean(object, key, default_val='Not found'):
    value = object.get(key, default_val)
    if type(value) is str:
        cleaned_val = value.strip().replace('\n', '').replace('\r', '')
        return cleaned_val
    return value


MONGO_URI = 'mongodb://localhost:27017'
MONGO_DATABASE = 'col-scienti-dev'
MONGO_COLLECTION = 'groups'

client = MongoClient(MONGO_URI)
db = client[MONGO_DATABASE]
groups_colletion = db[MONGO_COLLECTION]

valid_products = [
    'Artículos publicados', 'Libros publicados',
    'Capítulos de libro publicados'
]
query = {"products.category": {'$in': valid_products}}
projection = {
    'knowledgeArea': 1,
    'universityName': 1,
    'Category': 1,
    'products': 1,
    'groupName': 1,
    'gruplacURL': 1
}

groups_result = groups_colletion.find(query, projection)
total_products = 0
total_valid_products = 0
# print(groups_result[0])
for group in groups_result:
    for product in group['products']:
        total_products += 1
        if product['category'].strip() in valid_products:
            total_valid_products += 1
            product_data = {
                'university': get_and_clean(group, 'universityName'),
                'groupName': get_and_clean(group, 'groupName'),
                'groupKnowledgeArea': get_and_clean(group, 'knowledgeArea'),
                'groupClassification': get_and_clean(group, 'Category'),
                'productType': get_and_clean(product, 'category'),
                'productTitle': get_and_clean(product, 'title'),
                'productYear': get_and_clean(product, 'year'),
                'approved': get_and_clean(product, 'isApproved')
            }
            if not product_data['productTitle']:
                print(product)
                print(group['gruplacURL'])
            valid_products.append(product_data)
report_df = pd.DataFrame(valid_products)
report_df.to_csv('products_resport2.csv', index=False)

print(f'Total scanned products: {total_products}')
print(f'Total valid products: {total_valid_products}')