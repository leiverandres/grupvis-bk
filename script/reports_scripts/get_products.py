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
        'bigKnowledgeArea': 1,
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
                    'groupCode':
                    get_and_clean(group, 'code'),
                    'groupName':
                    get_and_clean(group, 'groupName'),
                    'groupKnowledgeArea':
                    get_and_clean(group, 'bigKnowledgeArea'),
                    'groupClassification':
                    get_and_clean(group, 'classification'),
                    'productType':
                    get_and_clean(product, 'category'),
                    'productTitle':
                    get_and_clean(product, 'title'),
                    'productYear':
                    get_and_clean(product, 'year'),
                    'approved':
                    get_and_clean(product, 'isApproved')
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
        'groupCode', 'groupName', 'groupKnowledgeArea', 'groupClassification',
        'productType', 'productTitle', 'productYear', 'approved'
    ]
    report_df = pd.DataFrame(valid_products, columns=columns)
    report_df.to_csv('products_report.csv', index=False)

    logging.info(f'Total scanned products: {total_products}')
    logging.info(f'Total valid products: {total_valid_products}')
