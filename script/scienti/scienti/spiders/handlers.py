import re


def articulos_publicados(unprocessed_data):
    '''
    Table name in gruolac: "Artículos publicados"
    Products table index: 1
    '''
    mixed_data_regex = re.compile(
        r'^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+), ?(?P<publisher>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_ ]+) ?ISSN: (?P<issn>\d{4}-\d{3}[\dx00X]|\d+)?, ?(?P<year>\d{4})? ?vol: ?(?P<vol>([aA][Ññ][oO] ?)?(\d+|N/A|n/a|[CMDIXLV]+))? ?fasc: (?P<fasc>(\d+|[Nn]/?7?[Aa]))? ?págs: (?P<pags>([\d\w]+|N/A|n/a)?[- ]*([\d\w]+|N/A|n/a)?)?,?'
    )
    data = {}
    data['type'] = unprocessed_data[1].strip(': ')
    data['title'] = unprocessed_data[2].strip()
    mixed_data_line = re.sub("[ \n]+", " ", unprocessed_data[3]).strip()
    data['doi'] = unprocessed_data[5].strip()
    data['authors'] = unprocessed_data[6].split(':')[1].strip(', \n')

    ## get mixed_data_line data
    match = mixed_data_regex.match(mixed_data_line)
    if match:
        data['country'] = match.group('country')
        data['publisher'] = match.group('publisher')
        data['issn'] = match.group('issn')
        data['year'] = match.group('year')
        data['vol'] = match.group('vol')
        data['fasc'] = match.group('fasc')
        data['pags'] = match.group('pags')
    return data


def libros_publicados(unprocessed_data):
    '''
    Table name in gruolac: "Libros publicados" and " Otros Libros publicados "
    Products table index: 2 and 7
    '''
    mixed_data_regex = re.compile(
        r'^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+), ?(?P<year>\d{4})?, ?ISBN: (?P<isbn>[\d\- ]+) ?vol: (?P<vol>([aA][Ññ][oO] ?)?(\d+|N/A|n/a|[CMDIXLV]+))? ?págs: ?(?P<pags>([\d\w]+|N/A|n/a)?[- ]*([\d\w]+|N/A|n/a)?)?, ?Ed. ?(?P<editorial>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_ ]+)'
    )
    data = {}
    data['type'] = unprocessed_data[1].strip()
    data['title'] = unprocessed_data[2].strip(': ')
    data['authors'] = unprocessed_data[4].split(':')[1].strip(', \n')
    mixed_data_line = re.sub("[ \n]+", " ", unprocessed_data[3]).strip()
    mixed_data_line = re.sub("[ \n]+", " ", mixed_data_line)
    match = mixed_data_regex.match(mixed_data_line)
    if match:
        data['country'] = match.group('country')
        data['year'] = match.group('year')
        data['isbn'] = match.group('isbn')
        data['vol'] = match.group('vol')
        data['pags'] = match.group('pags')
        data['editorial'] = match.group('editorial')
    return data


def capitulos_libro_publicado(unprocessed_data):
    '''
    Table name in gruolac: "Capítulos de libro publicados "
    Products table index: 3
    '''
    mixed_data_regex = re.compile(
        r'^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+), ?(?P<year>\d{4})?, ?(?P<book>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_ ]+), ?ISBN: (?P<isbn>[\d\- ]+), ?Vol. (?P<vol>([aA][Ññ][oO] ?)?(\d+|N/A|n/a|[CMDIXLV]+))?, ?págs: ?(?P<pags>([\d\w]+|N/A|n/a)?[- ]*([\d\w]+|N/A|n/a)?)?, ?Ed. ?(?P<editorial>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_ ]+)'
    )
    data = {}
    data['type'] = unprocessed_data[1].strip()
    data['title'] = unprocessed_data[2].strip(': ')
    data['authors'] = unprocessed_data[4].split(':')[1].strip(', \n')
    mixed_data_line = re.sub("[ \n]+", " ", unprocessed_data[3]).strip()

    match = mixed_data_regex.match(mixed_data_line)
    if match:
        data['country'] = match.group('country')
        data['year'] = match.group('year')
        data['book'] = match.group('book')
        data['isbn'] = match.group('isbn')
        data['vol'] = match.group('vol')
        data['pags'] = match.group('pags')
        data['editorial'] = match.group('editorial')
    return data


def documentos_trabajo(unprocessed_data):
    '''
    Table name in gruolac: "Documentos de trabajo"
    Products table index: 4
    '''
    mixed_data_regex = re.compile(
        r'^(?P<year>\d{4}), Nro. Paginas: ?(?P<nro_pags>\d+)?, Instituciones participantes: ?(?P<institutions>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_,;& ]+)?, URL: ?(?P<url>[\w:/.?=#$%-_]+)?, DOI: ?(?P<doi>[\w:/.?=#$%-]+)?'
    )
    data = {}
    data['type'] = unprocessed_data[1].strip()
    data['title'] = unprocessed_data[2].strip(': ')
    data['authors'] = unprocessed_data[4].split(':')[1].strip(', \n')
    mixed_data_line = re.sub("[ \n]+", " ", unprocessed_data[3]).strip()

    match = mixed_data_regex.match(mixed_data_line)
    if match:
        data['url'] = match.group('url')
        data['nroPags'] = match.group('nro_pags')
        data['doi'] = match.group('doi')
        data['institutions'] = match.group('institutions')
        data['year'] = match.group('year')
    return data


def otra_publicacion_divulgativa(unprocessed_data):
    '''
    Table name in gruolac: "Otra publicación divulgativa"
    Products table index: 5
    '''
    mixed_data_regex = re.compile(
        r'^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+), ?(?P<year>\d{4})?,.*')
    data = {}
    data['type'] = unprocessed_data[1].strip()
    data['title'] = unprocessed_data[2].strip(': ')
    data['authors'] = unprocessed_data[4].split(':')[1].strip(', \n')
    mixed_data_line = re.sub("[ \n]+", " ", unprocessed_data[3]).strip()
    match = mixed_data_regex.match(mixed_data_line)
    if match:
        data['country'] = match.group('country')
        data['year'] = match.group('year')
    return data


def otros_articulos_publicados(unprocessed_data):
    '''
    Table name in gruplac: "Otros artículos publicados"
    Products table index: 6
    '''
    mixed_data_regex = re.compile(
        r'^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+)?, ?(?P<publisher>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_ ]+)? ?ISSN: (?P<issn>\d{4}-\d{3}[\dx00X]|\d+)?, ?(?P<year>\d{4})? ?vol: ?(?P<vol>([aA][Ññ][oO] ?)?(\d+|N/A|n/a|[CMDIXLV]+))? ?fasc: ?(?P<fasc>(\d+|[Nn]/?7?[Aa]))? ?págs: (?P<pags>([\d\w]+|N/A|n/a)?[- ]*([\d\w]+|N/A|n/a)?)?,?'
    )
    data = {}
    data['type'] = unprocessed_data[1].strip(': ')
    data['title'] = unprocessed_data[2].strip()
    data['authors'] = unprocessed_data[4].split(':')[1].strip(', \n')
    mixed_data_line = re.sub("[ \n]+", " ", unprocessed_data[3]).strip()

    ## get mixed_data_line data
    match = mixed_data_regex.match(mixed_data_line)
    if match:
        data['country'] = match.group('country')
        data['publisher'] = match.group('publisher')
        data['issn'] = match.group('issn')
        data['year'] = match.group('year')
        data['vol'] = match.group('vol')
        data['fasc'] = match.group('fasc')
        data['pags'] = match.group('pags')
    return data


def traducciones(unprocessed_data):
    '''
    Table name in gruolac: "Traducciones"
    Products table index: 8
    '''
    mixed_data_regex = re.compile(
        r'^(?P<year>\d{4}), ?Revista: ?(?P<magazine>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_ ]+)? ?ISSN ?(?P<issn>\d{4}-\d{3}[\dx00X]|\d+)?, ?Libro: ?(?P<book>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_ ]+)? ?ISBN ?(?P<isbn>[\d\- ]+)?, ?Medio de divulgación: ?(?P<media>[\wáéíóúñÁÉÍÓÚÑ ]+)?'
    )
    data = {}
    data['type'] = unprocessed_data[1].strip()
    data['title'] = unprocessed_data[2].strip(': ')
    languages = unprocessed_data[4].strip(',\n ').split(',')
    data['originalLanguage'] = languages[0].split(':')[1].strip()
    data['translationLanguage'] = languages[1].split(':')[1].strip()
    data['authors'] = unprocessed_data[6].split(':')[1].strip(', \n')
    mixed_data_line = re.sub("[ \n]+", " ", unprocessed_data[3]).strip()
    match = mixed_data_regex.match(mixed_data_line)
    if match:
        data['year'] = match.group('year')
        data['magazine'] = match.group('magazine')
        data['issn'] = match.group('issn')
        data['book'] = match.group('book')
        data['isbn'] = match.group('isbn')
        data['media'] = match.group('media')
    return data


def cartas_mapas_similares(unprocessed_data):
    '''
    Table name in gruolac: "Cartas, mapas o similares"
    Products table index: 10
    '''
    mixed_data_regex = re.compile(
        r'^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+), ?(?P<year>\d{4})?, ?Institución financiadora: ?(?P<financing_institution>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_,;& ]+)?, ?Tema: ?(?P<topic>[\wáéíóúñÁÉÍÓÚÑ ]+)?'
    )
    data = {}
    data['type'] = unprocessed_data[1].strip()
    data['title'] = unprocessed_data[2].strip(': ')
    data['authors'] = unprocessed_data[4].split(':')[1].strip(', \n')
    mixed_data_line = re.sub("[ \n]+", " ", unprocessed_data[3]).strip()
    match = mixed_data_regex.match(mixed_data_line)
    if match:
        data['country'] = match.group('country')
        data['year'] = match.group('year')
        data['financingInstitution'] = match.group('financing_institution')
        data['topic'] = match.group('topic')
    return data


def consultorias(unprocessed_data):
    '''
    Table name in gruolac: "Consultorías científico tecnológicas e Informes técnicos"
    Products table index: 11
    '''
    mixed_data_regex = re.compile(
        r'^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+), ?(?P<year>\d{4})?, ?Idioma: ?(?P<language>[\wáéíóúñÁÉÍÓÚÑ ]+)?, ?Disponibilidad: ?(?P<availability>[\wáéíóúñÁÉÍÓÚÑ ]+)?, ?Número del contrato: ?(?P<contract_number>[\wáéíóúñÁÉÍÓÚÑ°.:\- ]+)?'
    )
    data = {}
    data['type'] = unprocessed_data[1].strip()
    data['title'] = unprocessed_data[2].strip(': ')
    data['beneficiaryInstitution'] = unprocessed_data[4].split(':')[1].strip()
    data['authors'] = unprocessed_data[5].split(':')[1].strip(', \n')
    mixed_data_line = re.sub("[ \n]+", " ", unprocessed_data[3]).strip()
    match = mixed_data_regex.match(mixed_data_line)
    if match:
        data['country'] = match.group('country')
        data['year'] = match.group('year')
        data['language'] = match.group('language')
        data['availability'] = match.group('availability')
        data['contractNumber'] = match.group('contract_number')
    return data


def disenos_innovacion(unprocessed_data):
    '''
    Table name in gruolac: "Diseños industriales", "Esquemas de trazados de circuito integrado", 
                           "Innovaciones en Procesos y Procedimientos", 
                           "Innovaciones generadas en la Gestión Empresarial" and "Prototipos"
    Products table index: 12, 13, 14, 15 and 20
    '''
    mixed_data_regex = re.compile(
        r'^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+), ?(?P<year>\d{4})?, ?Disponibilidad: ?(?P<availability>[\wáéíóúñÁÉÍÓÚÑ ]+)?, ?Institución financiadora: ?(?P<funding_institution>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_,;& ]+)?'
    )
    data = {}
    data['type'] = unprocessed_data[1].strip()
    data['title'] = unprocessed_data[2].strip(': ')
    data['authors'] = unprocessed_data[4].split(':')[1].strip(', \n')
    mixed_data_line = re.sub("[ \n]+", " ", unprocessed_data[3]).strip()
    match = mixed_data_regex.match(mixed_data_line)
    if match:
        data['country'] = match.group('country')
        data['year'] = match.group('year')
        data['availability'] = match.group('availability')
        data['fundingInstitution'] = match.group('funding_institution')
    return data


def nuevas_variedades_animal(unprocessed_data):
    mixed_data_regex = re.compile(
        r'^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+), ?(?P<year>\d{4})?, ?Acto administrativo del ICA: ?(?P<ica_admin_act>[\wáéíóúñÁÉÍÓÚÑ ]+)?, ?Institución financiadora: ?(?P<funding_institution>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_,;& ]+)?'
    )
    data = {}
    data['type'] = unprocessed_data[1].strip()
    data['title'] = unprocessed_data[2].strip(': ')
    data['authors'] = unprocessed_data[4].split(':')[1].strip(', \n')
    mixed_data_line = re.sub("[ \n]+", " ", unprocessed_data[3]).strip()
    match = mixed_data_regex.match(mixed_data_line)
    if match:
        data['country'] = match.group('country')
        data['year'] = match.group('year')
        data['ICAAdminAct'] = match.group('ica_admin_act')
        data['fundingInstitution'] = match.group('funding_institution')
    return data


def nuevas_variedades_vegetal(unprocessed_data):
    '''
    Table name in gruolac: "Nuevas variedades vegetal"
    Products table index: 17
    '''
    mixed_data_regex = re.compile(
        r'^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+), ?(?P<year>\d{4})?, ?Tipo de ciclo: ?(?P<cycle_type>[\wáéíóúñÁÉÍÓÚÑ ]+)?, ?Sitio web: ?(?P<web>[\w:/.?=#$%-_]+)?'
    )
    data = {}
    data['type'] = unprocessed_data[1].strip()
    data['title'] = unprocessed_data[2].strip(': ')
    data['fundingInstitution'] = unprocessed_data[4].split(':')[1].strip()
    data['authors'] = unprocessed_data[5].split(':')[1].strip(', \n')
    mixed_data_line = re.sub("[ \n]+", " ", unprocessed_data[3]).strip()
    match = mixed_data_regex.match(mixed_data_line)
    if match:
        data['country'] = match.group('country')
        data['year'] = match.group('year')
        data['cycleType'] = match.group('cycle_type')
        data['web'] = match.group('web')
    return data


def plantas_piloto_otros_productos(unprocessed_data):
    '''
    Esta función puede usarse con 'Plantas piloto' y 'Otros productos tecnológicos'
    '''
    mixed_data_regex = re.compile(
        r'^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+), ?(?P<year>\d{4})?, ?Disponibilidad: ?(?P<availability>[\wáéíóúñÁÉÍÓÚÑ ]+)?, ?Nombre comercial: ?(?P<tradename>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_,;& ]+)?'
    )
    data = {}
    data['type'] = unprocessed_data[1].strip()
    data['title'] = unprocessed_data[2].strip(': ')
    data['fundingInstitution'] = unprocessed_data[4].split(':')[1].strip()
    data['authors'] = unprocessed_data[5].split(':')[1].strip(', \n')
    mixed_data_line = re.sub("[ \n]+", " ", unprocessed_data[3]).strip()
    match = mixed_data_regex.match(mixed_data_line)
    if match:
        data['country'] = match.group('country')
        data['year'] = match.group('year')
        data['availability'] = match.group('availability')
        data['tradename'] = match.group('tradename')
    return data


def regulaciones_normas_guias(unprocessed_data):
    '''
    Table name in gruplac: "Regulaciones y Normas", "Guias de práctica clínica"and "Proyectos de ley"
    Products table index: 21, 23 and 24
    '''
    mixed_data_regex = re.compile(
        r'^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+), ?(?P<year>\d{4})?, ?Ambito: ?(?P<ambit>[\wáéíóúñÁÉÍÓÚÑ ]+)?, Fecha de publicación: ?(?P<publish_date>[\d:\-. ]+)?, ?Objeto: ?(?P<purpose>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_,;& ]+)?'
    )
    data = {}
    data['type'] = unprocessed_data[1].strip()
    data['title'] = unprocessed_data[2].strip(': ')
    data['fundingInstitution'] = unprocessed_data[4].split(':')[1].strip(
        ', \n')
    data['authors'] = unprocessed_data[5].split(':')[1].strip(', \n')
    mixed_data_line = re.sub("[ \n]+", " ", unprocessed_data[3]).strip()
    match = mixed_data_regex.match(mixed_data_line)
    if match:
        data['country'] = match.group('country')
        data['year'] = match.group('year')
        data['ambit'] = match.group('ambit')
        data['publishDate'] = match.group('publish_date')
        data['purpose'] = match.group('purpose')
    return data


def reglamentos_tecnicos(unprocessed_data):
    mixed_data_regex = re.compile(
        r'^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+), ?(?P<year>\d{4})?, ?Disponibilidad: ?(?P<availability>[\wáéíóúñÁÉÍÓÚÑ ]+)?, ?Sitio web: ?(?P<web>[\w:/.?=#$%-_]+)?'
    )
    data = {}
    data['type'] = unprocessed_data[1].strip()
    data['title'] = unprocessed_data[2].strip(': ')
    data['fundingInstitution'] = unprocessed_data[4].split(':')[1].strip()
    data['authors'] = unprocessed_data[5].split(':')[1].strip(', \n')
    mixed_data_line = re.sub("[ \n]+", " ", unprocessed_data[3]).strip()
    match = mixed_data_regex.match(mixed_data_line)
    if match:
        data['country'] = match.group('country')
        data['year'] = match.group('year')
        data['availability'] = match.group('availability')
        data['web'] = match.group('web')
    return data


def signos_distintivos(unprocessed_data):
    mixed_data_regex = re.compile(
        r'^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+), ?(?P<year>\d{4})?, ?Número del registro: ?(?P<registry_number>[\wáéíóúñÁÉÍÓÚÑ.°:\- ]+)?, ?Nombre del titular:(?P<holder>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_ ]+)?'
    )
    data = {}
    data['type'] = unprocessed_data[1].strip()
    data['title'] = unprocessed_data[2].strip(': ')
    mixed_data_line = re.sub("[ \n]+", " ", unprocessed_data[3]).strip()
    match = mixed_data_regex.match(mixed_data_line)
    if match:
        data['country'] = match.group('country')
        data['year'] = match.group('year')
        data['holder'] = match.group('holder')
        data['registryNumber'] = match.group('registry_number')
    return data


def softwares(unprocessed_data):
    '''
    Table name in gruolac: "Reglamentos técnicos" and "Softwares"
    Products table index: 22 and 26
    '''
    mixed_data_regex = re.compile(
        r'^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+), ?(?P<year>\d{4})?, ?Disponibilidad: ?(?P<availability>[\wáéíóúñÁÉÍÓÚÑ ]+)?, ?Sitio web: ?(?P<web>[\w:/.?=#$%-_]+)?'
    )
    data = {}
    data['type'] = unprocessed_data[1].strip()
    data['title'] = unprocessed_data[2].strip(': ')
    data['tradename'] = unprocessed_data[4].split(':')[1].strip()
    data['fundingInstitution'] = unprocessed_data[5].split(':')[1].strip()
    data['authors'] = unprocessed_data[6].split(':')[1].strip(', \n')
    mixed_data_line = re.sub("[ \n]+", " ", unprocessed_data[3]).strip()
    match = mixed_data_regex.match(mixed_data_line)
    if match:
        data['country'] = match.group('country')
        data['year'] = match.group('year')
        data['availability'] = match.group('availability')
        data['web'] = match.group('web')
    return data


def empresas_base_tecnologica(unprocessed_data):
    mixed_data_regex = re.compile(
        r'^(?P<month>[\wáéíóúñÁÉÍÓÚÑ]+)? ?(?P<year>\d{4})?, ?NIT: ?(?P<nit>[\d-]+)?, Fecha de registro ante cámara: (?P<registry_date>[\d:\-. ]+)?'
    )
    data = {}
    data['type'] = unprocessed_data[1].strip()
    data['title'] = unprocessed_data[2].strip(': ')
    data['authors'] = unprocessed_data[5].split(':')[1].strip(',\n ')
    mixed_data_line = re.sub("[ \n]+", " ", unprocessed_data[3]).strip()
    match = mixed_data_regex.match(mixed_data_line)
    if match:
        data['month'] = match.group('month')
        data['year'] = match.group('year')
        data['nit'] = match.group('nit')
        data['registryDate'] = match.group('registry_date')
    return data


def ediciones(unprocessed_data):
    mixed_data_regex = re.compile(
        r'^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+), ?(?P<year>\d{4})?, ?Editorial: ?(?P<editorial>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_ ]+)?, ?Idiomas: ?(?P<languages>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_,;& ]+)?, ?Páginas: ?(?P<nro_pags>\d+)?'
    )
    data = {}
    data['type'] = unprocessed_data[1].strip()
    data['title'] = unprocessed_data[2].strip(': ')
    data['authors'] = unprocessed_data[4].split(':')[1].strip(', \n')
    mixed_data_line = re.sub("[ \n]+", " ", unprocessed_data[3]).strip()
    match = mixed_data_regex.match(mixed_data_line)
    if match:
        data['country'] = match.group('country')
        data['year'] = match.group('year')
        data['editorial'] = match.group('editorial')
        data['languages'] = match.group('languages')
        data['nro_pags'] = match.group('nro_pags')
    return data


def eventos_cientificos(unprocessed_data):
    '''
    Falta extraer las instituciones asociadas
    '''
    mixed_data_regex = re.compile(
        r'^(?P<city>[\wáéíóúñÁÉÍÓÚÑ,. ]+), ?desde ?(?P<start_date>[\d:\-. ]+)? ?- ?hasta ?(?P<end_date>[\d:\-. ]+)? ?Ámbito: ?(?P<ambit>[\wáéíóúñÁÉÍÓÚÑ ]+)?, ?Tipos de participación: ?(?P<participation_type>[\wáéíóúñÁÉÍÓÚÑ ]+)?'
    )
    data = {}
    data['type'] = unprocessed_data[1].strip()
    data['title'] = unprocessed_data[2].strip(': ')
    mixed_data_line = re.sub("[ \n]+", " ", unprocessed_data[3]).strip()
    match = mixed_data_regex.match(mixed_data_line)
    if match:
        data['city'] = match.group('city')
        data['startDate'] = match.group('start_date')
        data['endDate'] = match.group('end_date')
        data['ambit'] = match.group('ambit')
        data['participationType'] = match.group('participation_type')
    return data


def informes_investigacion(unprocessed_data):
    mixed_data_regex = re.compile(
        r'^(?P<year>\d{4})?, ?Proyecto de investigación: ?(?P<research_project>[\wáéíóúñÁÉÍÓÚÑ:.,\-()\'"_ ]+)?'
    )
    data = {}
    data['type'] = unprocessed_data[1].strip()
    data['title'] = unprocessed_data[2].strip(': ')
    mixed_data_line = re.sub("[ \n]+", " ", unprocessed_data[3]).strip()
    data['authors'] = unprocessed_data[4].split(':')[1].strip(',\n ')
    match = mixed_data_regex.match(mixed_data_line)
    if match:
        data['year'] = match.group('year')
        data['researchProject'] = match.group('research_project')
    return data


def redes_conocimiento(unprocessed_data):
    mixed_data_regex = re.compile(
        r'^en ?(?P<city>[\wáéíóúñÁÉÍÓÚÑ,. ]+), ?desde ?(?P<start_date>[\d:\-. ]+)? - hasta?(?P<end_date>[\d:\-. ]+)?'
    )
    data = {}
    data['title'] = unprocessed_data[1].strip()
    data['networkLocation'] = unprocessed_data[2].strip(': ')
    mixed_data_line = re.sub("[ \n]+", " ", unprocessed_data[3]).strip()
    data['nroParticipantes'] = unprocessed_data[4].split(':')[1].strip(',\n ')
    match = mixed_data_regex.match(mixed_data_line)
    if match:
        data['city'] = match.group('city')
        data['startDate'] = match.group('start_date')
        data['endDate'] = match.group('end_date')
    return data


def contenido_impreso(unprocessed_data):
    mixed_data_regex = re.compile(
        r'^(?P<date>[\d:\-. ]+)?, ?Ambito: ?(?P<ambit>[\wáéíóúñÁÉÍÓÚÑ ]+)?, ?Medio de circulación: ?(?P<media>[\wáéíóúñÁÉÍÓÚÑ ]+)?'
    )
    second_mixed_data_regex = re.compile(
        r'^Lugar de publicación: (?P<place>.*), Sitio web: (?P<web>.*)')
    data = {}
    data['type'] = unprocessed_data[1].strip()
    data['title'] = unprocessed_data[2].strip(': ')
    mixed_data_line_1 = re.sub("[ \n]+", " ", unprocessed_data[3]).strip()
    mixed_data_line_2 = re.sub("[ \n]+", " ", unprocessed_data[4]).strip()
    data['authors'] = unprocessed_data[5].split(':')[1].strip(',\n ')
    match = mixed_data_regex.match(mixed_data_line_1)
    second_match = second_mixed_data_regex.match(mixed_data_line_2)
    if match:
        data['date'] = match.group('date')
        data['ambit'] = match.group('ambit')
        data['media'] = match.group('media')
    if second_match:
        data['place'] = second_match.group('place')
        data['web'] = second_match.group('web')
    return data


def contenido_multimedia(unprocessed_data):
    first_mixed_data_regex = re.compile(
        r'^(?P<year>\d{4})?, ?(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+)?, ?Idioma: ?(?P<language>[\wáéíóúñÁÉÍÓÚÑ ]+)?'
    )
    second_mixed_data_regex = re.compile(
        r'^Medio de divulgación: ?(?P<media>.+)?, ?Sitio web: ?(?P<web>.+)?')
    third_mixed_data_regex = re.compile(
        r'^ Emisora: ?(?P<emitter>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_ ]+)?, ?Instituciones participantes: (?P<institutions>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_,;& ]+)?'
    )
    data = {}
    data['type'] = unprocessed_data[1].strip()
    data['title'] = unprocessed_data[2].strip(': ')
    mixed_data_line_1 = re.sub("[ \n]+", " ", unprocessed_data[3]).strip()
    mixed_data_line_2 = re.sub("[ \n]+", " ", unprocessed_data[4]).strip()
    mixed_data_line_3 = re.sub("[ \n]+", " ", unprocessed_data[5]).strip()
    data['authors'] = unprocessed_data[6].split(':')[1].strip(',\n ')
    first_match = first_mixed_data_regex.match(mixed_data_line_1)
    second_match = second_mixed_data_regex.match(mixed_data_line_2)
    third_match = third_mixed_data_regex.match(mixed_data_line_3)
    if first_match:
        data['year'] = first_match.group('year')
        data['country'] = first_match.group('country')
        data['language'] = first_match.group('language')
    if second_match:
        data['media'] = second_match.group('media')
        data['web'] = second_match.group('web')
    if third_match:
        data['emitter'] = third_match.group('emitter')
        data['institutions'] = third_match.group('institutions')
    return data


def contenido_virtual(unprocessed_data):
    mixed_data_regex = re.compile(
        r'^(?P<date>[\d:\-. ]+)?, ?Entidades vinculadas: ?(?P<entities>.+)?, ?Sitio web: ?(?P<web>[\w:/.?=#$%-_]+)?'
    )
    data = {}
    data['type'] = unprocessed_data[1].strip()
    data['title'] = unprocessed_data[2].strip(': ')
    mixed_data_line = re.sub("[ \n]+", " ", unprocessed_data[3]).strip()
    data['authors'] = unprocessed_data[4].split(':')[1].strip(',\n ')
    match = mixed_data_regex.match(mixed_data_line)
    if match:
        data['date'] = match.group('date')
        data['entities'] = match.group('entities')
        data['web'] = match.group('web')
    return data


def estrategias(unprocessed_data):
    '''
    Es usada para 'Estrategias de Comunicación del Conocimiento',
    'Estrategias Pedagógicas para el fomento a la CTI' y
    'Participación Ciudadana en Proyectos de CTI'
    '''
    dates_patter = re.compile(
        r'^desde ?(?P<start_month>[\wáéíóúñÁÉÍÓÚÑ]+)? (?P<start_year>\d{4})? hasta ?(?P<end_month>[\wáéíóúñÁÉÍÓÚÑ]+)? ?(?P<end_year>\d{4})?'
    )
    data = {}
    data['title'] = unprocessed_data[1].strip()
    dates = re.sub("[ \n]+", " ", unprocessed_data[2]).strip()
    data['description'] = unprocessed_data[3].split(':')[1].strip()
    match = dates_patter.match(dates)
    if match:
        data['year'] = match.group('start_year')
        data['startYear'] = match.group('start_year')
        data['startMonth'] = match.group('start_month')
        data['endYear'] = match.group('end_year')
        data['endMonth'] = match.group('end_month')
    return data


def espacios_participacion(unprocessed_data):
    dates_patter = re.compile(
        r'^desde ?(?P<start_date>[\d:\-. ]+)? ?- ?hasta ?(?P<end_date>[\d:\-. ]+)? ?Número de participantes: (?P<nro_participants>.+)?, Página web: ?(?P<web>.+)?'
    )
    data = {}
    data['title'] = unprocessed_data[1].strip()
    data['city'] = unprocessed_data[2].strip(': ')
    mixed_data_line = re.sub("[ \n]+", " ", unprocessed_data[3]).strip()
    match = dates_patter.match(mixed_data_line)
    if match:
        data['startDate'] = match.group('start_date')
        data['endDate'] = match.group('end_date')
        data['nroParticipants'] = match.group('nro_participants')
        data['web'] = match.group('web')
    return data


def obras_productos(unprocessed_data):
    '''
    This is a subtable of: "Producción en arte, arquitectura y diseño"
    SubTable name in gruplac: "Obras o productos"
    Products table index: 40.1
    '''
    mixed_data_regex = re.compile(
        r'^Fecha de creación: ?(?P<month>[\D]+) de (?P<year>\d{4}) Disciplina o ámbito de origen: (?P<ambit>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_,;& ]+)?'
    )
    data = {}
    data['title'] = unprocessed_data[0].split(':')[1].strip(',\n ')
    mixed_data_line = re.sub("[ \n]+", " ", unprocessed_data[1]).strip()
    match = mixed_data_regex.match(mixed_data_line)
    if match:
        data['year'] = match.group('year')
        data['month'] = match.group('month')
        data['ambit'] = match.group('ambit')
    return data


def industrias_creativas_culturales(unprocessed_data):
    '''
    This is a subtable of: "Producción en arte, arquitectura y diseño"
    SubTable name in gruplac: "Industrias creativas y culturales"
    Products table index: 40.2
    '''
    first_mixed_data_regex = re.compile(
        r'^Nombre de la empresa creativa o cultural: ?(?P<title>[\wáéíóúñÁÉÍÓÚÑ ]+)?, ?NIT o código de registro:?(?P<nit>[\d:\-. ]+)?'
    )
    second_mixed_data_regex = re.compile(
        r'^Fecha de registro ante la cámara de comercio: ?(?P<registration_date>[\d:\-. ]+)?, ?Tiene productos en el mercado: ?(?P<has_product>.*)'
    )
    mixed_data_line_1 = re.sub("[ \n]+", " ", unprocessed_data[0]).strip()
    mixed_data_line_2 = re.sub("[ \n]+", " ", unprocessed_data[1]).strip()
    first_match = first_mixed_data_regex.match(mixed_data_line_1)
    second_match = second_mixed_data_regex.match(mixed_data_line_2)
    data = {}
    if first_match:
        data['title'] = first_match.group('title')
        data['nit'] = first_match.group('nit')
    if second_match:
        data['registrationDate'] = second_match.group('registration_date')
        data['hasProduct'] = second_match.group('has_product')
    return data


def eventos_artisticos(unprocessed_data):
    '''
    This is a subtable of: "Producción en arte, arquitectura y diseño"
    SubTable name in gruplac: "Eventos Artísticos"
    Products table index: 40.3
    '''
    dates_regex = re.compile(
        r'^Fecha de inicio: ?(?P<start_date>[\d:\-. ]+)?, ?Fecha de finalización: ?(?P<end_date>[\d:\-. ]+)?'
    )
    data = {}
    data['title'] = unprocessed_data[0].split(':')[1].strip('\n ')
    data['description'] = unprocessed_data[2].split(':')[1].strip('\n ')
    mixed_data_line = re.sub("[ \n]+", " ", unprocessed_data[1]).strip()
    match = dates_regex.match(mixed_data_line)
    if match:
        data['startDate'] = match.group('start_date')
        data['endDate'] = match.group('end_date')
    return data


def talleres_creacion(unprocessed_data):
    '''
    This is a subtable of: "Producción en arte, arquitectura y diseño"
    SubTable name in gruplac: "Talleres de Creación"
    Products table index: 40.4
    '''
    first_mixed_data_regex = re.compile(
        r'^Nombre del taller: ?(?P<title>.+) ?,Tipo de taller: ?(?P<workshop_type>.+)?,Participación: (?P<participation>.+)? '
    )
    second_mixed_data_regex = re.compile(
        r'^Fecha de inicio: ?(?P<start_date>[\d:\-. ]+)?, ?Fecha de finalización: ?(?P<end_date>[\d:\-. ]+)?'
    )
    third_mixed_data_regex = re.compile(
        r'^Ámbito: ?(?P<ambit>[\wáéíóúñÁÉÍÓÚÑ ]+)?,Distinción obtenida: ?(?P<obtained_distinction>.+)?, ?Mecanismo de selección: ?(?P<selection_mechanism>.+)?'
    )
    data = {}
    data['place'] = unprocessed_data[2].split(':')[1].strip()
    mixed_data_line_1 = re.sub("[ \n]+", " ", unprocessed_data[0]).strip()
    mixed_data_line_2 = re.sub("[ \n]+", " ", unprocessed_data[1]).strip()
    mixed_data_line_3 = re.sub("[ \n]+", " ", unprocessed_data[3]).strip()
    first_match = first_mixed_data_regex.match(mixed_data_line_1)
    second_match = second_mixed_data_regex.match(mixed_data_line_2)
    third_match = third_mixed_data_regex.match(mixed_data_line_3)
    if first_match:
        data['title'] = first_match.group('title')
        data['workshopType'] = first_match.group('workshop_type')
        data['participation'] = first_match.group('participation')
    if second_match:
        data['startDate'] = second_match.group('start_date')
        data['endDate'] = second_match.group('end_date')
    if third_match:
        data['ambit'] = third_match.group('ambit')
        data['obtainedDistinction'] = third_match.group('obtained_distinction')
        data['selectionMechanism'] = third_match.group('selection_mechanism')
    return data


def asesorias_programa_ondas(unprocessed_data):
    mixed_data_regex = re.compile(
        r'^desde ?(?P<start_date>[\d:\-. ]+)? ?hasta ?(?P<end_date>[\d:\-. ]+)?, Participó en feria (?P<type>[\wáéíóúñÁÉÍÓÚÑ ]+)?, Nombre de las ferias:(?P<fairs>.*)'
    )
    data = {}
    data['title'] = unprocessed_data[1].strip()
    data['city'] = unprocessed_data[2].strip(': ')
    mixed_data_line = re.sub("[ \n]+", " ", unprocessed_data[3]).strip()
    data['institution'] = unprocessed_data[4].split(':')[1].strip()
    match = mixed_data_regex.match(mixed_data_line)
    if match:
        data['startDate'] = match.group('start_date')
        data['year'] = data['startDate'].split('-')[0]
        data['endDate'] = match.group('end_date')
        data['type'] = match.group('type')
        data['fairs'] = match.group('fairs')
    return data


def curso_corto(unprocessed_data):
    first_mixed_data_regex = re.compile(
        r'^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+)?, (?P<year>\d{4})?, ?Idioma: ?(?P<language>[\wáéíóúñÁÉÍÓÚÑ ]+)?, ?Medio de divulgación: ?(?P<media>[\wáéíóúñÁÉÍÓÚÑ ]+)?'
    )
    second_mixed_data_regex = re.compile(
        r'^Sitio web: ?(?P<web>[\w:/.?=#$%-_]+)?, ?Participación como (?P<participation_type>[\wáéíóúñÁÉÍÓÚÑ ]+)?, Duración \(semanas\): (?P<weeks>.*)?, Finalidad: (?P<purpose>.+)?'
    )
    third_mixed_data_regex = re.compile(
        r'^Lugar: (?P<place>.+)?, ?Institución financiadora: ?(?P<institution>.+)?'
    )
    data = {}
    data['type'] = unprocessed_data[1].strip()
    data['title'] = unprocessed_data[2].strip(': ')
    mixed_data_line_1 = re.sub("[ \n]+", " ", unprocessed_data[3]).strip()
    mixed_data_line_2 = re.sub("[ \n]+", " ", unprocessed_data[4]).strip()
    mixed_data_line_3 = re.sub("[ \n]+", " ", unprocessed_data[5]).strip()
    data['authors'] = unprocessed_data[6].split(':')[1].strip()
    first_match = first_mixed_data_regex.match(mixed_data_line_1)
    second_match = second_mixed_data_regex.match(mixed_data_line_2)
    third_match = third_mixed_data_regex.match(mixed_data_line_3)
    if first_match:
        data['country'] = first_match.group('country')
        data['year'] = first_match.group('year')
        data['language'] = first_match.group('language')
        data['media'] = first_match.group('media')
    if second_match:
        data['web'] = second_match.group('web')
        data['participationType'] = second_match.group('participation_type')
        data['weeks'] = second_match.group('weeks')
        data['purpose'] = second_match.group('purpose')
    if third_match:
        data['place'] = third_match.group('place')
        data['institution'] = third_match.group('institution')
    return data


def trabajos_dirigidos(unprocessed_data):
    first_mixed_data_regex = re.compile(
        r'^Desde ?(?P<start_month>[\wáéíóúñÁÉÍÓÚÑ]+)? (?P<start_year>\d{4})? hasta ?(?P<end_month>[\wáéíóúñÁÉÍÓÚÑ]+)? ?(?P<end_year>\d{4})?, ?Tipo de orientación: ?(?P<orientation_type>.+)?'
    )
    second_mixed_data_regex = re.compile(
        r'^Nombre del estudiante: ?(?P<student_names>.+)?, ?Programa académico: ?(?P<academic_program>.+)?'
    )
    third_mixed_data_regex = re.compile(
        r'^Número de páginas: (?P<nro_pags>.+)?, ?Valoración: ?(?P<calification>.+)?, ?Institución: ?(?P<institution>.*)'
    )
    data = {}
    data['type'] = unprocessed_data[1].strip()
    data['title'] = unprocessed_data[2].strip(': ')
    mixed_data_line_1 = re.sub("[ \n]+", " ", unprocessed_data[3]).strip()
    mixed_data_line_2 = re.sub("[ \n]+", " ", unprocessed_data[4]).strip()
    mixed_data_line_3 = re.sub("[ \n]+", " ", unprocessed_data[5]).strip()
    data['authors'] = unprocessed_data[6].split(':')[1].strip()
    first_match = first_mixed_data_regex.match(mixed_data_line_1)
    second_match = second_mixed_data_regex.match(mixed_data_line_2)
    third_match = third_mixed_data_regex.match(mixed_data_line_3)
    if first_match:
        data['year'] = first_match.group('start_year')
        data['startYear'] = first_match.group('start_year')
        data['startMonth'] = first_match.group('start_month')
        data['endYear'] = first_match.group('end_year')
        data['endMonth'] = first_match.group('end_month')
        data['orientationType'] = first_match.group('orientation_type')
    if second_match:
        data['studentNames'] = second_match.group('student_names')
        data['academicProgram'] = second_match.group('academic_program')
    if third_match:
        data['nroPags'] = third_match.group('nro_pags')
        data['calification'] = third_match.group('calification')
        data['institution'] = third_match.group('institution')
    return data


def jurado_evaluadores_trabajos(unprocessed_data):
    '''
    Table name in gruplac: "Jurado/Comisiones evaluadoras de trabajo de grado"
    '''
    first_mixed_data_regex = re.compile(
        r'^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+)?, ?(?P<year>\d{4})?, ?Idioma: ?(?P<language>[\wáéíóúñÁÉÍÓÚÑ ]+)?, ?Medio de divulgación: ?(?P<media>[\wáéíóúñÁÉÍÓÚÑ ]+)?'
    )
    second_mixed_data_regex = re.compile(
        r'^Sitio web: ?(?P<web>.+)?, ?Nombre del orientado: ?(?P<oriented_people>.+)?'
    )
    third_mixed_data_regex = re.compile(
        r'^Programa académico: ?(?P<academic_program>.+)?, ?Institución: ?(?P<institution>.+)?'
    )
    data = {}
    data['type'] = unprocessed_data[1].strip()
    data['title'] = unprocessed_data[2].strip(': ')
    mixed_data_line_1 = re.sub("[ \n]+", " ", unprocessed_data[3]).strip()
    mixed_data_line_2 = re.sub("[ \n]+", " ", unprocessed_data[4]).strip()
    mixed_data_line_3 = re.sub("[ \n]+", " ", unprocessed_data[5]).strip()
    data['authors'] = unprocessed_data[6].split(':')[1].strip()
    first_match = first_mixed_data_regex.match(mixed_data_line_1)
    second_match = second_mixed_data_regex.match(mixed_data_line_2)
    third_match = third_mixed_data_regex.match(mixed_data_line_3)
    if first_match:
        data['country'] = first_match.group('country')
        data['year'] = first_match.group('year')
        data['language'] = first_match.group('language')
        data['media'] = first_match.group('media')
    if second_match:
        data['web'] = second_match.group('web')
        data['orientedPeople'] = second_match.group('oriented_people')
    if third_match:
        data['academicProgram'] = third_match.group('academic_program')
        data['institution'] = third_match.group('institution')
    return data


def participacion_comites_evalucacion(unprocessed_data):
    first_mixed_data_regex = re.compile(
        r'^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+)?, ?(?P<year>\d{4})?, ?Sitio web: ?(?P<web>.+)?'
    )
    second_mixed_data_regex = re.compile(
        r'^Medio de divulgación: ?(?P<media>.+)?, ?Institución: ?(?P<institution>.+)?'
    )
    data = {}
    data['type'] = unprocessed_data[1].strip()
    data['title'] = unprocessed_data[2].strip(': ')
    mixed_data_line_1 = re.sub("[ \n]+", " ", unprocessed_data[3]).strip()
    mixed_data_line_2 = re.sub("[ \n]+", " ", unprocessed_data[4]).strip()
    data['authors'] = unprocessed_data[5].split(':')[1].strip()
    first_match = first_mixed_data_regex.match(mixed_data_line_1)
    second_match = second_mixed_data_regex.match(mixed_data_line_2)
    if first_match:
        data['country'] = first_match.group('country')
        data['year'] = first_match.group('year')
        data['web'] = first_match.group('web')
    if second_match:
        data['media'] = second_match.group('media')
        data['institution'] = second_match.group('institution')
    return data


def demas_trabajos(unprocessed_data):
    mixed_data_regex = re.compile(
        r'^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+)?, ?(?P<year>\d{4})?, ?Idioma: (?P<language>[\wáéíóúñÁÉÍÓÚÑ ]+)?, ?Medio de divulgación: ?(?P<media>.+)?'
    )
    data = {}
    data['type'] = unprocessed_data[1].strip()
    data['title'] = unprocessed_data[2].strip(': ')
    mixed_data_line = re.sub("[ \n]+", " ", unprocessed_data[3]).strip()
    data['authors'] = unprocessed_data[4].split(':')[1].strip()
    match = mixed_data_regex.match(mixed_data_line)
    if match:
        data['country'] = match.group('country')
        data['year'] = match.group('year')
        data['language'] = match.group('language')
        data['media'] = match.group('media')
    return data


def proyectos(unprocessed_data):
    dates_patter = re.compile(
        r'^(?P<start_year>\d{4})?/(?P<start_month>\d+)? ?- ?(?P<end_year>\d{4})?/?(?P<end_month>\d+)?'
    )
    data = {}
    data['type'] = unprocessed_data[1].strip()
    data['title'] = unprocessed_data[2].strip(': ')
    if len(unprocessed_data) > 3:
        mixed_data_line = re.sub("[ \n]+", " ", unprocessed_data[3]).strip()
        match = dates_patter.match(mixed_data_line)
        if match:
            data['year'] = match.group('start_year')
            data['startYear'] = match.group('start_year')
            data['startMonth'] = match.group('start_month')
            data['endYear'] = match.group('end_year')
            data['endMonth'] = match.group('end_month')
    return data


HANDLERS = {
    'Artículos publicados':
    articulos_publicados,
    'Libros publicados':
    libros_publicados,
    'Capítulos de libro publicados':
    capitulos_libro_publicado,
    'Documentos de trabajo':
    documentos_trabajo,
    'Otra publicación divulgativa':
    otra_publicacion_divulgativa,
    'Otros artículos publicados':
    otros_articulos_publicados,
    'Otros Libros publicados':
    libros_publicados,
    'Traducciones':
    traducciones,
    'Cartas, mapas o similares':
    cartas_mapas_similares,
    'Consultorías científico tecnológicas e Informes técnicos':
    consultorias,
    'Diseños industriales':
    disenos_innovacion,
    'Esquemas de trazados de circuito integrado':
    disenos_innovacion,
    'Innovaciones en Procesos y Procedimientos':
    disenos_innovacion,
    'Innovaciones generadas en la Gestión Empresarial':
    disenos_innovacion,
    'Nuevas variedades animal':
    nuevas_variedades_animal,
    'Nuevas variedades vegetal':
    nuevas_variedades_vegetal,
    'Plantas piloto':
    plantas_piloto_otros_productos,
    'Otros productos tecnológicos':
    plantas_piloto_otros_productos,
    'Prototipos':
    disenos_innovacion,
    'Regulaciones y Normas':
    regulaciones_normas_guias,
    'Reglamentos técnicos':
    reglamentos_tecnicos,
    'Guias de práctica clínica':
    regulaciones_normas_guias,
    'Proyectos de ley':
    regulaciones_normas_guias,
    'Signos distintivos':
    signos_distintivos,
    'Softwares':
    softwares,
    'Empresas de base tecnológica':
    empresas_base_tecnologica,
    'Ediciones':
    ediciones,
    'Eventos Científicos':
    eventos_cientificos,
    'Informes de investigación':
    informes_investigacion,
    'Redes de Conocimiento Especializado':
    redes_conocimiento,
    'Generación de Contenido Impreso':
    contenido_impreso,
    'Generación de Contenido Multimedia':
    contenido_multimedia,
    'Generación de Contenido Virtual':
    contenido_virtual,
    'Estrategias de Comunicación del Conocimiento':
    estrategias,
    'Estrategias Pedagógicas para el fomento a la CTI':
    estrategias,
    'Espacios de Participación Ciudadana':
    espacios_participacion,
    'Participación Ciudadana en Proyectos de CTI':
    estrategias,
    'Obras o productos':
    obras_productos,
    'Industrias creativas y culturales':
    industrias_creativas_culturales,
    'Eventos Artísticos':
    eventos_artisticos,
    'Talleres de Creación':
    talleres_creacion,
    'Asesorías al Programa Ondas':
    asesorias_programa_ondas,
    'Curso de Corta Duración Dictados':
    curso_corto,
    'Trabajos dirigidos/turorías':
    trabajos_dirigidos,
    'Jurado/Comisiones evaluadoras de trabajo de grado':
    jurado_evaluadores_trabajos,
    'Participación en comités de evaluación':
    participacion_comites_evalucacion,
    'Demás trabajos':
    demas_trabajos,
    'Proyectos':
    proyectos
}
