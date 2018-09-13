from pymongo import MongoClient

MONGO_URI = 'mongodb://localhost:27017'
MONGO_DATABASE = 'col-scienti-dev'
MONGO_COLLECTION = 'groups'

PRODUCT_TYPES = [
    'Artículos', 'Libros', 'Capítulos', 'Documentos', 'Otra', 'Otros', 'Otros',
    'Traducciones', 'Cartas', 'Consultorías', 'Diseños', 'Esquemas',
    'Innovaciones', 'Innovaciones', 'Nuevas', 'Nuevas', 'Plantas', 'Otros',
    'Prototipos', 'Regulaciones', 'Reglamentos', 'Guias', 'Proyectos',
    'Signos', 'Softwares', 'Empresas', 'Ediciones', 'Eventos', 'Informes',
    'Redes', 'Generación', 'Generación', 'Generación', 'Estrategias',
    'Estrategias', 'Espacios', 'Participación', 'Obras', 'Industrias',
    'Eventos', 'Talleres', 'Asesorías', 'Curso', 'Trabajos', 'Jurado',
    'Participación', 'Demás', 'Proyectos'
]

counter_map = {}

if __name__ == '__main__':
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DATABASE]
    groups_colletion = db[MONGO_COLLECTION]

    count = groups_colletion.find().count()
    print(count)
