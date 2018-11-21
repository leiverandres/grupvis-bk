from pymongo import MongoClient
import pandas as pd
from progress.bar import Bar
import copy
from collections import Counter
import logging

logger = logging.getLogger(__name__)

MONGO_URI = 'mongodb://localhost:27017'
MONGO_DATABASE = 'col-scienti-dev'
MONGO_COLLECTION = 'summaryProfiles'

KNOWLEDGE_AREAS = [
    'Ingeniería y Tecnología', 'Ciencias Naturales',
    'Ciencias Médicas y de la Salud', 'Ciencias Sociales',
    'Ciencias Agrícolas', 'Humanidades'
]

CLASSIFICATIONS = ['A1', 'A', 'B', 'C', 'reconocido']


def connect_to_db():
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DATABASE]
    collection = db[MONGO_COLLECTION]
    return collection


if __name__ == '__main__':
    summary_collection = connect_to_db()
    df = pd.read_csv('./dataset.csv')
    for area in KNOWLEDGE_AREAS:
        for classification in CLASSIFICATIONS:
            cluster = df[(df['knowledgeArea'] == area)
                         & (df['classification'] == classification)]
            cluster_values = cluster.drop(
                ['knowledgeArea', 'classification', 'code'], axis=1)
            mean_values = cluster_values.mean()

            summary_row = {
                'classification': classification,
                'bigKnowledgeArea': area,
                'meanValues': mean_values.values.squeeze().tolist(),
                'order': mean_values.index.tolist()
            }
            summary_collection.insert_one(summary_row)
    print('DONE')
