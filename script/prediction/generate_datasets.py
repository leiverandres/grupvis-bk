from pymongo import MongoClient
import pandas as pd
from progress.bar import Bar
import copy
from collections import Counter
import logging

logger = logging.getLogger(__name__)

MONGO_URI = 'mongodb://localhost:27017'
MONGO_DATABASE = 'col-scienti'
MONGO_COLLECTION = 'groups'
PRODUCT_TYPES = [
    'Artículos publicados', 'Libros publicados',
    'Capítulos de libro publicados', 'Documentos de trabajo',
    'Otra publicación divulgativa', 'Otros artículos publicados',
    'Otros Libros publicados', 'Traducciones', 'Cartas, mapas o similares',
    'Consultorías científico tecnológicas e Informes técnicos',
    'Diseños industriales', 'Esquemas de trazados de circuito integrado',
    'Innovaciones en Procesos y Procedimientos',
    'Innovaciones generadas en la Gestión Empresarial',
    'Nuevas variedades animal', 'Nuevas variedades vegetal', 'Plantas piloto',
    'Otros productos tecnológicos', 'Prototipos', 'Regulaciones y Normas',
    'Reglamentos técnicos', 'Guias de práctica clínica', 'Proyectos de ley',
    'Signos distintivos', 'Softwares', 'Empresas de base tecnológica',
    'Ediciones', 'Eventos Científicos', 'Informes de investigación',
    'Redes de Conocimiento Especializado', 'Generación de Contenido Impreso',
    'Generación de Contenido Multimedia', 'Generación de Contenido Virtual',
    'Estrategias de Comunicación del Conocimiento',
    'Estrategias Pedagógicas para el fomento a la CTI',
    'Espacios de Participación Ciudadana',
    'Participación Ciudadana en Proyectos de CTI', 'Obras o productos',
    'Industrias creativas y culturales', 'Eventos Artísticos',
    'Talleres de Creación', 'Asesorías al Programa Ondas',
    'Curso de Corta Duración Dictados', 'Trabajos dirigidos/turorías',
    'Jurado/Comisiones evaluadoras de trabajo de grado',
    'Participación en comités de evaluación', 'Demás trabajos', 'Proyectos',
    'Producción en arte, arquitectura y diseño'
]

ADITIONAL_FIELDS = ['code', 'knowledgeArea', 'category', 'bigKnowledgeArea']


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


def init_counter():
    init_val = 0
    counter = Counter({p: init_val for p in PRODUCT_TYPES})
    return counter


if __name__ == '__main__':
    groups_collection = connect_to_db()
    all_groups = groups_collection.find()
    total_groups = copy.copy(all_groups).count()
    bar = Bar('Processing products', max=total_groups)
    df = pd.DataFrame(columns=[*ADITIONAL_FIELDS, *PRODUCT_TYPES])
    for group in all_groups:
        products_counter = init_counter()
        arr_types = map(lambda p: p['category'], group['products'])
        products_counter.update(arr_types)
        aditional = {key: group[key] for key in ADITIONAL_FIELDS}
        row_data = {**dict(products_counter), **aditional}
        df = df.append(row_data, ignore_index=True)
        bar.next()
    bar.finish()
    df.to_csv('dataset.csv')
    print('DONE')
