from pymongo import MongoClient
import pandas as pd
from progress.bar import Bar
from functools import reduce
from collections import Counter
import logging

logger = logging.getLogger(__name__)

MONGO_URI = 'mongodb://localhost:27017'
MONGO_DATABASE = 'col-scienti'
MONGO_COLLECTION = 'groups'

BASE_FIELDS = [
    'code', 'groupName', 'classification', 'bigKnowledgeArea', 'knowledgeArea'
]

PROJECTION_FIELDS = BASE_FIELDS + ['products']

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

PRODUCT_TYPES_COLS = [
    product_type + ' sin aprobar' for product_type in PRODUCT_TYPES
] + PRODUCT_TYPES

DF_COLUMNS = [*BASE_FIELDS, *PRODUCT_TYPES_COLS]


def connect_to_db():
    client = MongoClient(MONGO_URI)
    groups_collection = client[MONGO_DATABASE][MONGO_COLLECTION]
    return groups_collection


def get_and_clean(object, key, default_val='Not found'):
    value = object.get(key, default_val)
    if type(value) is str:
        cleaned_val = value.strip().replace('\n', '').replace('\r', '')
        return cleaned_val
    return value


def init_counter():
    init_val = 0
    counter = Counter({p: init_val for p in PRODUCT_TYPES_COLS})
    return counter


def filter_year(product):
    try:
        product_year = product['year']
        if product_year is None:
            return False
        return int(product_year) >= 2012 and int(product_year) <= 2016
    except KeyError:
        # This happens when product doesn't have year info
        return False


def filter_approved(product):
    return filter_year(product) and product['isApproved']


def filter_non_approved(product):
    return filter_year(product) and not product['isApproved']


if __name__ == '__main__':
    groups_collection = connect_to_db()

    query = {"institution": "Universidad Tecnológica De Pereira - Utp"}
    projection = {field: 1 for field in PROJECTION_FIELDS}
    groups_result = groups_collection.find(query, projection)

    total_groups = groups_collection.count_documents(query)
    dataset = pd.DataFrame(columns=DF_COLUMNS)
    print('Total groups: {}'.format(total_groups))
    bar = Bar('Processing groups', max=total_groups)
    for group in groups_result:
        bar.next()
        row_data = {field: group[field] for field in BASE_FIELDS}
        not_approved_types = list(
            map(lambda p: p['category'] + ' sin aprobar',
                filter(filter_non_approved, group['products'])))
        approved_types = list(
            map(lambda p: p['category'],
                filter(filter_approved, group['products'])))
        products_counter = init_counter()
        products_counter.update(approved_types + not_approved_types)
        row_data.update(dict(products_counter))
        dataset = dataset.append(row_data, ignore_index=True)
    bar.finish()
    dataset.to_csv('utp_products_resport.csv', index=False)
