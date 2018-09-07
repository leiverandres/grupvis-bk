from pymongo import MongoClient
import pandsa as pd

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
    'groupName': 1
}

groups_result = groups_colletion.find(query, projection)
for group in groups_result:
    for product in group['products']:
        product_data = {
            'university': group['universityName'],
            'groupKnowledgeArea': group['knowledgeArea'],
            'groupClassification': group['Category'],
            'groupName': group['groupName'],
            'productType': product['type']
        }