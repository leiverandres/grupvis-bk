from pymongo import MongoClient
import pandas as pd
from progress.bar import Bar
import copy
from collections import Counter
import logging
from scipy import spatial

logger = logging.getLogger(__name__)

MONGO_URI = 'mongodb://localhost:27017'
MONGO_DATABASE = 'col-scienti-dev'
MONGO_COLLECTION = 'groups'

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


def get_target_classification(classification):
    if classification == 'A1':
        return 'A1'
    if classification == 'A':
        return 'A1'
    elif classification == 'B':
        return 'A'
    elif classification == 'C':
        return 'B'
    elif classification == 'reconocido':
        return 'C'


def check_clusters(df):
    for area in KNOWLEDGE_AREAS:
        for classification in CLASSIFICATIONS:
            cluster = df[(df['knowledgeArea'] == area)
                         & (df['classification'] == classification)]
            print('Area: {}, Classification {}, Cluster Shape {}'.format(
                area, classification, cluster.shape))


if __name__ == '__main__':
    groups_collection = connect_to_db()
    df = pd.read_csv('dataset.csv')
    # check_clusters(df)
    # exit()
    query = {"institution": "Universidad Tecnológica De Pereira - Utp"}
    utp_groups = groups_collection.find(query)
    bar = Bar('Processing groups', max=86)
    for group in utp_groups:
        group_code = group['code']
        group_knowledge_area = group['bigKnowledgeArea']
        group_classification = group['classification']
        group_profile = df[df['code'] == group_code]
        group_sumary = group_profile.drop(
            ['knowledgeArea', 'classification', 'code'], axis=1)
        print('Group code: ', group_code)
        print('Group knowledge area: ', group_knowledge_area)
        print('Group classification', group_classification)
        target_classification = get_target_classification(group_classification)
        print('Target classification', target_classification)
        ## Assuming we're gonna compare to an upper group
        upper_cluster = df[(df['knowledgeArea'] == group_knowledge_area)
                           & (df['classification'] == target_classification) &
                           (df['code'] != 'COL0035995')]
        cluster_data = upper_cluster.drop(
            ['knowledgeArea', 'classification', 'code'], axis=1)
        print('cluster size', cluster_data.shape)
        print('hey')
        tree = spatial.KDTree(cluster_data)
        closest = tree.query(group_sumary.values)
        closest_group = upper_cluster.iloc[closest[1], :]
        closest_group_values = closest_group.drop(
            ['knowledgeArea', 'classification', 'code'], axis=1)
        print('Closest group:', closest_group)
        closest_info = {
            'targetClassification': target_classification,
            'bigKnowledgeArea': group_knowledge_area,
            'closestValues': closest_group_values.values.squeeze().tolist(),
            'order': closest_group_values.columns.tolist()
        }
        groups_collection.update({
            'code': group_code
        }, {'$set': {
            'closestGroupInfo': closest_info
        }})
        bar.next()
    bar.finish()
    print('DONE')
