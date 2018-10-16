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
    'code', 'IS', 'I', 'IJ', 'ED', 'EM', 'JI', 'EP', 'IVD', 'IVM', 'IVP',
    'IVE', 'IV', 'classification'
]
dataset = pd.DataFrame(columns=COLUMNS)
total_groups = groups_collection.count_documents({})
bar = Bar('Processing groups', max=total_groups)
for group in groups_collection.find({}):
    row_data = {
        'code': group['code'],
        'classification': group['classification']
    }
    profiles = group['profiles']
    members_profile = profiles['members_profile_table']
    for row in members_profile['rows_values']:
        row_data[row['abreviatura']] = row['Valor del indicador para el Grupo']
    dataset = dataset.append([row_data])
    bar.next()
dataset.to_csv('perfil_integrantes.csv', index=False)
bar.finish()
print('DONE')
