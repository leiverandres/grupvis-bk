from pymongo import MongoClient
import pandas as pd
from progress.bar import Bar

MONGO_URI = 'mongodb://localhost:27017'
MONGO_DATABASE = 'col-scienti-dev'
MONGO_COLLECTION = 'groups'
client = MongoClient(MONGO_URI)
scienti_db = client[MONGO_DATABASE]
groups_collection = scienti_db[MONGO_COLLECTION]
COLUMNS = [
    'IS', 'I', 'IJ', 'ED', 'EM', 'JI', 'EP', 'IVD', 'IVM', 'IVP', 'IVE', 'IV',
    'IC', 'ICOOP', 'ART_A', 'ART_D', 'LIB', 'CAP', 'PAT', 'VV', 'AAD', 'TEC',
    'EMP', 'RNL', 'CON', 'MR', 'PCI', 'EPF', 'CCO', 'CCE', 'TD', 'TM', 'TG',
    'PID', 'PF', 'PERS', 'AP', 'APO', 'knowledgeArea', 'classification', 'code'
]
dataset = pd.DataFrame(columns=COLUMNS)
total_groups = groups_collection.count_documents({})
bar = Bar('Processing groups', max=total_groups)
for group in groups_collection.find({}):
    profiles = group['profiles']
    row_data = {
        'classification': group['classification'],
        'code': group['code'],
        'knowledgeArea': group['bigKnowledgeArea']
    }
    summary = {'values': [], 'order': []}
    for profile_name in profiles.keys():
        cur_profile = profiles[profile_name]
        for row in cur_profile['rows_values']:
            summary['values'].append(row['Valor del indicador para el Grupo'])
            summary['order'].append(row['abreviatura'])
            row_data[row['abreviatura']] = row[
                'Valor del indicador para el Grupo']
    print(summary)
    print(group['_id'])
    groups_collection.update({
        '_id': group['_id']
    }, {'$set': {
        'summary': summary
    }})
    dataset = dataset.append([row_data])
    bar.next()
dataset.to_csv('dataset.csv', index=False)
bar.finish()
print('DONE')