from pymongo import MongoClient
import pandas as pd
from progress.bar import Bar

MONGO_URI = 'mongodb://localhost:27017'
MONGO_DATABASE = 'col-scienti-dev'
MONGO_COLLECTION = 'groups'
client = MongoClient(MONGO_URI)
scienti_db = client[MONGO_DATABASE]
groups_collection = scienti_db[MONGO_COLLECTION]

COLUMNS = ['code', 'type', 'quantity']
query = {"institution": "Universidad Tecnológica De Pereira - Utp"}
total_groups = groups_collection.count_documents(query)
bar = Bar('Processing groups', max=total_groups)
for group in groups_collection.find(query):
    dataset = pd.DataFrame(columns=COLUMNS)
    profiles = group['profiles']
    members_profile = profiles['members_profile_table']
    for row in members_profile['rows_values']:
        row_data = {
            'code': group['code'],
            'type': row['abreviatura'],
            'quantity': row['Valor del indicador para el Grupo']
        }
        dataset = dataset.append([row_data])
    dataset.to_csv('./members_by_group/' + group['code'] + '.csv', index=False)
    bar.next()
bar.finish()
print('DONE')
