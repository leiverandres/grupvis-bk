import re


def articulos_publicados(data_extracted):
    extra_patter = re.compile(
        r'^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+),[ ]*(?P<publisher>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_ ]+)[ ]*ISSN: (?P<issn>\d{4}-\d{3}[\dx00X]|\d+)?, (?P<year>\d{4})?[ ]*vol: ?(?P<vol>([aA][Ññ][oO] ?)?(\d+|N/A|n/a|[CMDIXLV]+))?[ ]*fasc: (?P<fasc>(\d+|[Nn]/?7?[Aa]))?[ ]*págs: (?P<pags>([\d\w]+|N/A|n/a)?[- ]*([\d\w]+|N/A|n/a)?)?,?'
    )
    row_data = {}
    row_data['type'] = data_extracted[1].strip(': ')
    row_data['title'] = data_extracted[2].strip()
    extra = re.sub("[ \n]+", " ", data_extracted[3]).strip()
    row_data['doi'] = data_extracted[5].strip()
    row_data['authors'] = data_extracted[6].split(':')[1].strip(', ')

    ## get extra data
    match = extra_patter.match(extra)
    if match:
        row_data['country'] = match.group('country')
        row_data['publisher'] = match.group('publisher')
        row_data['issn'] = match.group('issn')
        row_data['year'] = match.group('year')
        row_data['vol'] = match.group('vol')
        row_data['fasc'] = match.group('fasc')
        row_data['pags'] = match.group('pags')
    return row_data


def libros_publicados(data_extracted):
    extra_patter = re.compile(
        r'^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+), ?(?P<year>\d{4})?, ?ISBN: (?P<isbn>[\d\- ]+) ?vol: (?P<vol>([aA][Ññ][oO] ?)?(\d+|N/A|n/a|[CMDIXLV]+))? ?págs: ?(?P<pags>([\d\w]+|N/A|n/a)?[- ]*([\d\w]+|N/A|n/a)?)?, ?Ed. ?(?P<editorial>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_ ]+)'
    )
    row_data = {}
    row_data['type'] = data_extracted[1].strip()
    row_data['title'] = data_extracted[2].strip(': ')
    row_data['authors'] = data_extracted[4].split(':')[1].strip(', ')
    extra = re.sub("[ \n]+", " ", data_extracted[3]).strip()
    extra = re.sub("[ \n]+", " ", extra)
    match = extra_patter.match(extra)
    if match:
        row_data['country'] = match.group('country')
        row_data['year'] = match.group('year')
        row_data['isbn'] = match.group('isbn')
        row_data['vol'] = match.group('vol')
        row_data['pags'] = match.group('pags')
        row_data['editorial'] = match.group('editorial')
    return row_data


def capitulos_libro_publicado(data_extracted):
    extra_patter = re.compile(
        r'^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+), ?(?P<year>\d{4})?, ?(?P<book>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_ ]+), ?ISBN: (?P<isbn>[\d\- ]+), ?Vol. (?P<vol>([aA][Ññ][oO] ?)?(\d+|N/A|n/a|[CMDIXLV]+))?, ?págs: ?(?P<pags>([\d\w]+|N/A|n/a)?[- ]*([\d\w]+|N/A|n/a)?)?, ?Ed. ?(?P<editorial>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_ ]+)'
    )
    row_data = {}
    row_data['type'] = data_extracted[1].strip()
    row_data['title'] = data_extracted[2].strip(': ')
    row_data['authors'] = data_extracted[4].split(':')[1].strip(', ')
    extra = re.sub("[ \n]+", " ", data_extracted[3]).strip()

    match = extra_patter.match(extra)
    if match:
        row_data['country'] = match.group('country')
        row_data['year'] = match.group('year')
        row_data['book'] = match.group('book')
        row_data['isbn'] = match.group('isbn')
        row_data['vol'] = match.group('vol')
        row_data['pags'] = match.group('pags')
        row_data['editorial'] = match.group('editorial')
    return row_data


def documentos_trabajo(data_extracted):
    extra_patter = re.compile(
        r'^(?P<year>\d{4}), Nro. Paginas: ?(?P<nro_pags>\d+)?, Instituciones participantes: ?(?P<institutions>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_,; ]+)?, URL: ?(?P<url>[\w:/.?=#$%-_]+)?, DOI: ?(?P<doi>[\w:/.?=#$%-]+)?'
    )
    row_data = {}
    row_data['type'] = data_extracted[1].strip()
    row_data['title'] = data_extracted[2].strip(': ')
    row_data['authors'] = data_extracted[4].split(':')[1].strip(', ')
    extra = re.sub("[ \n]+", " ", data_extracted[3]).strip()

    match = extra_patter.match(extra)
    if match:
        row_data['url'] = match.group('url')
        row_data['nroPags'] = match.group('nro_pags')
        row_data['doi'] = match.group('doi')
        row_data['institutions'] = match.group('institutions')
        row_data['year'] = match.group('year')
    return row_data


def otra_publicacion_divulgativa(data_extracted):
    extra_patter = re.compile(
        r'^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+), ?(?P<year>\d{4})?,.*')
    row_data = {}
    row_data['type'] = data_extracted[1].strip()
    row_data['title'] = data_extracted[2].strip(': ')
    row_data['authors'] = data_extracted[4].split(':')[1].strip(', ')
    extra = re.sub("[ \n]+", " ", data_extracted[3]).strip()
    match = extra_patter.match(extra)
    if match:
        row_data['country'] = match.group('country')
        row_data['year'] = match.group('year')
    return row_data


def traducciones(data_extracted):
    extra_patter = re.compile(
        r'^(?P<year>\d{4}), ?Revista: ?(?P<magazine>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_ ]+)? ?ISSN ?(?P<issn>\d{4}-\d{3}[\dx00X]|\d+)?, ?Libro: ?(?P<book>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_ ]+)? ?ISBN ?(?P<isbn>[\d\- ]+)?, ?Medio de divulgación: ?(?P<media>[\wáéíóúñÁÉÍÓÚÑ ]+)?'
    )
    row_data = {}
    row_data['type'] = data_extracted[1].strip()
    row_data['title'] = data_extracted[2].strip(': ')
    languages = data_extracted[4].strip(',\n ').split(',')
    row_data['originalLanguage'] = languages[0].split(':')[1].strip()
    row_data['translationLanguage'] = languages[1].split(':')[1].strip()
    row_data['authors'] = data_extracted[6].split(':')[1].strip(', ')
    first_extra = re.sub("[ \n]+", " ", data_extracted[3]).strip()
    match = extra_patter.match(first_extra)
    if match:
        row_data['year'] = match.group('year')
        row_data['magazine'] = match.group('magazine')
        row_data['issn'] = match.group('issn')
        row_data['book'] = match.group('book')
        row_data['isbn'] = match.group('isbn')
        row_data['media'] = match.group('media')
    return row_data


def otros_articulos_publicados(data_extracted):
    '''
    Table name in gruplac: "Otros artículos publicados"
    '''
    extra_patter = re.compile(
        r'^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+)?, ?(?P<publisher>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_ ]+)? ?ISSN: (?P<issn>\d{4}-\d{3}[\dx00X]|\d+)?, ?(?P<year>\d{4})? ?vol: ?(?P<vol>([aA][Ññ][oO] ?)?(\d+|N/A|n/a|[CMDIXLV]+))? ?fasc: ?(?P<fasc>(\d+|[Nn]/?7?[Aa]))? ?págs: (?P<pags>([\d\w]+|N/A|n/a)?[- ]*([\d\w]+|N/A|n/a)?)?,?'
    )
    row_data = {}
    row_data['type'] = data_extracted[1].strip(': ')
    row_data['title'] = data_extracted[2].strip()
    row_data['authors'] = data_extracted[4].split(':')[1].strip(', ')
    extra = re.sub("[ \n]+", " ", data_extracted[3]).strip()

    ## get extra data
    match = extra_patter.match(extra)
    if match:
        row_data['country'] = match.group('country')
        row_data['publisher'] = match.group('publisher')
        row_data['issn'] = match.group('issn')
        row_data['year'] = match.group('year')
        row_data['vol'] = match.group('vol')
        row_data['fasc'] = match.group('fasc')
        row_data['pags'] = match.group('pags')
    return row_data


def cartas_mapas_similares(data_extracted):
    extra_patter = re.compile(
        r'^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+), ?(?P<year>\d{4})?, ?Institución financiadora: ?(?P<financing_institution>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_,; ]+)?, ?Tema: ?(?P<topic>[\wáéíóúñÁÉÍÓÚÑ ]+)?'
    )
    row_data = {}
    row_data['type'] = data_extracted[1].strip()
    row_data['title'] = data_extracted[2].strip(': ')
    row_data['authors'] = data_extracted[4].split(':')[1].strip(', ')
    extra = re.sub("[ \n]+", " ", data_extracted[3]).strip()
    match = extra_patter.match(extra)
    if match:
        row_data['country'] = match.group('country')
        row_data['year'] = match.group('year')
        row_data['financingInstitution'] = match.group('financing_institution')
        row_data['topic'] = match.group('topic')
    return row_data


def consultorias(data_extracted):
    extra_patter = re.compile(
        r'^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+), ?(?P<year>\d{4})?, ?Idioma: ?(?P<language>[\wáéíóúñÁÉÍÓÚÑ ]+)?, ?Disponibilidad: ?(?P<availability>[\wáéíóúñÁÉÍÓÚÑ ]+)?, ?Número del contrato: ?(?P<contract_number>[\wáéíóúñÁÉÍÓÚÑ°.:\- ]+)?'
    )
    row_data = {}
    row_data['type'] = data_extracted[1].strip()
    row_data['title'] = data_extracted[2].strip(': ')
    row_data['beneficiaryInstitution'] = data_extracted[4].split(':')[
        1].strip()
    row_data['authors'] = data_extracted[5].split(':')[1].strip(', ')
    extra = re.sub("[ \n]+", " ", data_extracted[3]).strip()
    match = extra_patter.match(extra)
    if match:
        row_data['country'] = match.group('country')
        row_data['year'] = match.group('year')
        row_data['language'] = match.group('language')
        row_data['availability'] = match.group('availability')
        row_data['contractNumber'] = match.group('contract_number')
    return row_data


def disenos_innovacion(data_extracted):
    '''
    Esta función se puede aplicar a 'Diseños industriales',
    'Innovaciones en Procesos y Procedimientos' y 'Prototipos'
    '''
    extra_patter = re.compile(
        r'^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+), ?(?P<year>\d{4})?, ?Disponibilidad: ?(?P<availability>[\wáéíóúñÁÉÍÓÚÑ ]+)?, ?Institución financiadora: ?(?P<funding_institution>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_,; ]+)?'
    )
    row_data = {}
    row_data['type'] = data_extracted[1].strip()
    row_data['title'] = data_extracted[2].strip(': ')
    row_data['authors'] = data_extracted[4].split(':')[1].strip(', ')
    extra = re.sub("[ \n]+", " ", data_extracted[3]).strip()
    match = extra_patter.match(extra)
    if match:
        row_data['country'] = match.group('country')
        row_data['year'] = match.group('year')
        row_data['availability'] = match.group('availability')
        row_data['fundingInstitution'] = match.group('funding_institution')
    return row_data


def plantas_piloto_otros_productos(data_extracted):
    '''
    Esta función puede usarse con 'Plantas piloto' y 'Otros productos tecnológicos'
    '''
    extra_patter = re.compile(
        r'^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+), ?(?P<year>\d{4})?, ?Disponibilidad: ?(?P<availability>[\wáéíóúñÁÉÍÓÚÑ ]+)?, ?Nombre comercial: ?(?P<tradename>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_,; ]+)?'
    )
    row_data = {}
    row_data['type'] = data_extracted[1].strip()
    row_data['title'] = data_extracted[2].strip(': ')
    row_data['fundingInstitution'] = data_extracted[4].split(':')[1].strip()
    row_data['authors'] = data_extracted[5].split(':')[1].strip(', ')
    extra = re.sub("[ \n]+", " ", data_extracted[3]).strip()
    match = extra_patter.match(extra)
    if match:
        row_data['country'] = match.group('country')
        row_data['year'] = match.group('year')
        row_data['availability'] = match.group('availability')
        row_data['tradename'] = match.group('tradename')
    return row_data


def regulaciones_normas(data_extracted):
    extra_patter = re.compile(
        r'^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+), ?(?P<year>\d{4})?, ?Ambito: ?(?P<ambit>[\wáéíóúñÁÉÍÓÚÑ ]+)?, Fecha de publicación: ?(?P<publish_date>[\d:\-. ]+)?, ?Objeto: ?(?P<purpose>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_,; ]+)?'
    )
    row_data = {}
    row_data['type'] = data_extracted[1].strip()
    row_data['title'] = data_extracted[2].strip(': ')
    row_data['fundingInstitution'] = data_extracted[4].split(':')[1].strip()
    row_data['authors'] = data_extracted[5].split(':')[1].strip(', ')
    extra = re.sub("[ \n]+", " ", data_extracted[3]).strip()
    match = extra_patter.match(extra)
    if match:
        row_data['country'] = match.group('country')
        row_data['year'] = match.group('year')
        row_data['ambit'] = match.group('ambit')
        row_data['publishDate'] = match.group('publish_date')
        row_data['purpose'] = match.group('purpose')
    return row_data


def signos_distintivos(data_extracted):
    extra_patter = re.compile(
        r'^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+), ?(?P<year>\d{4})?, ?Número del registro: ?(?P<registry_number>[\wáéíóúñÁÉÍÓÚÑ.°:\- ]+)?, ?Nombre del titular:(?P<holder>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_ ]+)?'
    )
    row_data = {}
    row_data['type'] = data_extracted[1].strip()
    row_data['title'] = data_extracted[2].strip(': ')
    extra = re.sub("[ \n]+", " ", data_extracted[3]).strip()
    match = extra_patter.match(extra)
    if match:
        row_data['country'] = match.group('country')
        row_data['year'] = match.group('year')
        row_data['holder'] = match.group('holder')
        row_data['registryNumber'] = match.group('registry_number')
    return row_data


def softwares(data_extracted):
    extra_patter = re.compile(
        r'^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+), ?(?P<year>\d{4})?, ?Disponibilidad: ?(?P<availability>[\wáéíóúñÁÉÍÓÚÑ ]+)?, ?Sitio web: ?(?P<web>[\w:/.?=#$%-_]+)?'
    )
    row_data = {}
    row_data['type'] = data_extracted[1].strip()
    row_data['title'] = data_extracted[2].strip(': ')
    row_data['tradename'] = data_extracted[4].split(':')[1].strip()
    row_data['fundingInstitution'] = data_extracted[5].split(':')[1].strip()
    row_data['authors'] = data_extracted[6].split(':')[1].strip(', ')
    extra = re.sub("[ \n]+", " ", data_extracted[3]).strip()
    match = extra_patter.match(extra)
    if match:
        row_data['country'] = match.group('country')
        row_data['year'] = match.group('year')
        row_data['availability'] = match.group('availability')
        row_data['web'] = match.group('web')
    return row_data


def empresas_base_tecnologica(data_extracted):
    extra_patter = re.compile(
        r'^(?P<month>[\wáéíóúñÁÉÍÓÚÑ]+)? ?(?P<year>\d{4})?, ?NIT: ?(?P<nit>[\d-]+)?, Fecha de registro ante cámara: (?P<registry_date>[\d:\-. ]+)?'
    )
    row_data = {}
    row_data['type'] = data_extracted[1].strip()
    row_data['title'] = data_extracted[2].strip(': ')
    row_data['authors'] = data_extracted[5].split(':')[1].strip(',\n ')
    extra = re.sub("[ \n]+", " ", data_extracted[3]).strip()
    match = extra_patter.match(extra)
    if match:
        row_data['month'] = match.group('month')
        row_data['year'] = match.group('year')
        row_data['nit'] = match.group('nit')
        row_data['registryDate'] = match.group('registry_date')
    return row_data


def ediciones(data_extracted):
    extra_patter = re.compile(
        r'^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+), ?(?P<year>\d{4})?, ?Editorial: ?(?P<editorial>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_ ]+)?, ?Idiomas: ?(?P<languages>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_,; ]+)?, ?Páginas: ?(?P<nro_pags>\d+)?'
    )
    row_data = {}
    row_data['type'] = data_extracted[1].strip()
    row_data['title'] = data_extracted[2].strip(': ')
    row_data['authors'] = data_extracted[4].split(':')[1].strip(', ')
    extra = re.sub("[ \n]+", " ", data_extracted[3]).strip()
    match = extra_patter.match(extra)
    if match:
        row_data['country'] = match.group('country')
        row_data['year'] = match.group('year')
        row_data['editorial'] = match.group('editorial')
        row_data['languages'] = match.group('languages')
        row_data['nro_pags'] = match.group('nro_pags')
    return row_data


def eventos_cientificos(data_extracted):
    '''
    Falta extraer las instituciones asociadas
    '''
    extra_patter = re.compile(
        r'^(?P<city>[\wáéíóúñÁÉÍÓÚÑ,. ]+), ?desde ?(?P<start_date>[\d:\-. ]+)? ?- ?hasta ?(?P<end_date>[\d:\-. ]+)? ?Ámbito: ?(?P<ambit>[\wáéíóúñÁÉÍÓÚÑ ]+)?, ?Tipos de participación: ?(?P<participation_type>[\wáéíóúñÁÉÍÓÚÑ ]+)?'
    )
    row_data = {}
    row_data['type'] = data_extracted[1].strip()
    row_data['title'] = data_extracted[2].strip(': ')
    extra = re.sub("[ \n]+", " ", data_extracted[3]).strip()
    match = extra_patter.match(extra)
    if match:
        row_data['city'] = match.group('city')
        row_data['startDate'] = match.group('start_date')
        row_data['endDate'] = match.group('end_date')
        row_data['ambit'] = match.group('ambit')
        row_data['participationType'] = match.group('participation_type')
    return row_data


def informes_investigacion(data_extracted):
    extra_patter = re.compile(
        r'^(?P<year>\d{4})?, ?Proyecto de investigación: ?(?P<research_project>[\wáéíóúñÁÉÍÓÚÑ:.,\-()\'"_ ]+)?'
    )
    row_data = {}
    row_data['type'] = data_extracted[1].strip()
    row_data['title'] = data_extracted[2].strip(': ')
    extra = re.sub("[ \n]+", " ", data_extracted[3]).strip()
    row_data['authors'] = data_extracted[4].split(':')[1].strip(',\n ')
    match = extra_patter.match(extra)
    if match:
        row_data['year'] = match.group('year')
        row_data['researchProject'] = match.group('research_project')
    return row_data


def redes_conocimiento(data_extracted):
    extra_patter = re.compile(
        r'^en ?(?P<city>[\wáéíóúñÁÉÍÓÚÑ,. ]+), ?desde ?(?P<start_date>[\d:\-. ]+)? - hasta?(?P<end_date>[\d:\-. ]+)?'
    )
    row_data = {}
    row_data['title'] = data_extracted[1].strip()
    row_data['networkLocation'] = data_extracted[2].strip(': ')
    extra = re.sub("[ \n]+", " ", data_extracted[3]).strip()
    row_data['nroParticipantes'] = data_extracted[4].split(':')[1].strip(
        ',\n ')
    match = extra_patter.match(extra)
    if match:
        row_data['city'] = match.group('city')
        row_data['startDate'] = match.group('start_date')
        row_data['endDate'] = match.group('end_date')
    return row_data


def contenido_impreso(data_extracted):
    extra_patter = re.compile(
        r'^(?P<date>[\d:\-. ]+)?, ?Ambito: ?(?P<ambit>[\wáéíóúñÁÉÍÓÚÑ ]+)?, ?Medio de circulación: ?(?P<media>[\wáéíóúñÁÉÍÓÚÑ ]+)?'
    )
    second_extra_patter = re.compile(
        r'^Lugar de publicación: (?P<place>.*), Sitio web: (?P<web>.*)')
    row_data = {}
    row_data['type'] = data_extracted[1].strip()
    row_data['title'] = data_extracted[2].strip(': ')
    extra = re.sub("[ \n]+", " ", data_extracted[3]).strip()
    second_extra = re.sub("[ \n]+", " ", data_extracted[4]).strip()
    row_data['authors'] = data_extracted[5].split(':')[1].strip(',\n ')
    match = extra_patter.match(extra)
    second_match = second_extra_patter.match(second_extra)
    if match:
        row_data['date'] = match.group('date')
        row_data['ambit'] = match.group('ambit')
        row_data['media'] = match.group('media')
    if second_match:
        row_data['place'] = second_match.group('place')
        row_data['web'] = second_match.group('web')
    return row_data


def contenido_multimedia(data_extracted):
    first_extra_patter = re.compile(
        r'^(?P<year>\d{4})?, ?(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+)?, ?Idioma: ?(?P<language>[\wáéíóúñÁÉÍÓÚÑ ]+)?'
    )
    second_extra_patter = re.compile(r'^Medio de divulgación: ?(?P<media>.+)?, ?Sitio web: ?(?P<web>.+)?')
    third_extra_patter = re.compile(
        r'^ Emisora: ?(?P<emitter>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_ ]+)?, ?Instituciones participantes: (?P<institutions>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_,; ]+)?'
    )
    row_data = {}
    row_data['type'] = data_extracted[1].strip()
    row_data['title'] = data_extracted[2].strip(': ')
    first_extra = re.sub("[ \n]+", " ", data_extracted[3]).strip()
    second_extra = re.sub("[ \n]+", " ", data_extracted[4]).strip()
    third_extra = re.sub("[ \n]+", " ", data_extracted[5]).strip()
    row_data['authors'] = data_extracted[6].split(':')[1].strip(',\n ')
    first_match = first_extra_patter.match(first_extra)
    second_match = second_extra_patter.match(second_extra)
    third_match = third_extra_patter.match(third_extra)
    if first_match:
        row_data['year'] = first_match.group('year')
        row_data['country'] = first_match.group('country')
        row_data['language'] = first_match.group('language')
    if second_match:
        row_data['media'] = second_match.group('media')
        row_data['web'] = second_match.group('web')
    if third_match:
        row_data['emitter'] = third_match.group('emitter')
        row_data['institutions'] = third_match.group('institutions')
    return row_data


def contenido_virtual(data_extracted):
    extra_patter = re.compile(
        r'^(?P<date>[\d:\-. ]+)?, ?Entidades vinculadas: ?(?P<entities>.+)?, ?Sitio web: ?(?P<web>[\w:/.?=#$%-_]+)?'
    )
    row_data = {}
    row_data['type'] = data_extracted[1].strip()
    row_data['title'] = data_extracted[2].strip(': ')
    extra = re.sub("[ \n]+", " ", data_extracted[3]).strip()
    row_data['authors'] = data_extracted[4].split(':')[1].strip(',\n ')
    match = extra_patter.match(extra)
    if match:
        row_data['date'] = match.group('date')
        row_data['entities'] = match.group('entities')
        row_data['web'] = match.group('web')
    return row_data


def estrategias(data_extracted):
    '''
    Es usada para 'Estrategias de Comunicación del Conocimiento',
    'Estrategias Pedagógicas para el fomento a la CTI' y
    'Participación Ciudadana en Proyectos de CTI'
    '''
    dates_patter = re.compile(
        r'^desde ?(?P<start_month>[\wáéíóúñÁÉÍÓÚÑ]+)? (?P<start_year>\d{4})? hasta ?(?P<end_month>[\wáéíóúñÁÉÍÓÚÑ]+)? ?(?P<end_year>\d{4})?'
    )
    row_data = {}
    row_data['title'] = data_extracted[1].strip()
    dates = re.sub("[ \n]+", " ", data_extracted[2]).strip()
    row_data['description'] = data_extracted[3].split(':')[1].strip()
    match = dates_patter.match(dates)
    if match:
        row_data['year'] = match.group('start_year')
        row_data['startYear'] = match.group('start_year')
        row_data['startMonth'] = match.group('start_month')
        row_data['endYear'] = match.group('end_year')
        row_data['endMonth'] = match.group('end_month')
    return row_data


def espacios_participacion(data_extracted):
    dates_patter = re.compile(
        r'^desde ?(?P<start_date>[\d:\-. ]+)? ?- ?hasta ?(?P<end_date>[\d:\-. ]+)? ?Número de participantes: (?P<nro_participants>.+)?, Página web: ?(?P<web>.+)?'
    )
    row_data = {}
    row_data['title'] = data_extracted[1].strip()
    row_data['city'] = data_extracted[2].strip(': ')
    extra = re.sub("[ \n]+", " ", data_extracted[3]).strip()
    match = dates_patter.match(extra)
    if match:
        row_data['startDate'] = match.group('start_date')
        row_data['endDate'] = match.group('end_date')
        row_data['nroParticipants'] = match.group('nro_participants')
        row_data['web'] = match.group('web')
    return row_data


def asesorias_programa_ondas(data_extracted):
    extra_patter = re.compile(
        r'^desde ?(?P<start_date>[\d:\-. ]+)? ?hasta ?(?P<end_date>[\d:\-. ]+)?, Participó en feria (?P<type>[\wáéíóúñÁÉÍÓÚÑ ]+)?, Nombre de las ferias:(?P<fairs>.*)'
    )
    row_data = {}
    row_data['title'] = data_extracted[1].strip()
    row_data['city'] = data_extracted[2].strip(': ')
    extra = re.sub("[ \n]+", " ", data_extracted[3]).strip()
    row_data['institution'] = data_extracted[4].split(':')[1].strip()
    match = extra_patter.match(extra)
    if match:
        row_data['startDate'] = match.group('start_date')
        row_data['year'] = row_data['startDate'].split('-')[0]
        row_data['endDate'] = match.group('end_date')
        row_data['type'] = match.group('type')
        row_data['fairs'] = match.group('fairs')
    return row_data


def curso_corto(data_extracted):
    first_extra_patter = re.compile(
        r'^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+)?, (?P<year>\d{4})?, ?Idioma: ?(?P<language>[\wáéíóúñÁÉÍÓÚÑ ]+)?, ?Medio de divulgación: ?(?P<media>[\wáéíóúñÁÉÍÓÚÑ ]+)?'
    )
    second_extra_patter = re.compile(
        r'^Sitio web: ?(?P<web>[\w:/.?=#$%-_]+)?, ?Participación como (?P<participation_type>[\wáéíóúñÁÉÍÓÚÑ ]+)?, Duración \(semanas\): (?P<weeks>.*)?, Finalidad: (?P<purpose>.+)?'
    )
    third_extra_patter = re.compile(
        r'^Lugar: (?P<place>.+)?, ?Institución financiadora: ?(?P<institution>.+)?'
    )
    row_data = {}
    row_data['type'] = data_extracted[1].strip()
    row_data['title'] = data_extracted[2].strip(': ')
    first_extra = re.sub("[ \n]+", " ", data_extracted[3]).strip()
    second_extra = re.sub("[ \n]+", " ", data_extracted[4]).strip()
    third_extra = re.sub("[ \n]+", " ", data_extracted[5]).strip()
    row_data['authors'] = data_extracted[6].split(':')[1].strip()
    first_match = first_extra_patter.match(first_extra)
    second_match = second_extra_patter.match(second_extra)
    third_match = third_extra_patter.match(third_extra)
    if first_match:
        row_data['country'] = first_match.group('country')
        row_data['year'] = first_match.group('year')
        row_data['language'] = first_match.group('language')
        row_data['media'] = first_match.group('media')
    if second_match:
        row_data['web'] = second_match.group('web')
        row_data['participationType'] = second_match.group(
            'participation_type')
        row_data['weeks'] = second_match.group('weeks')
        row_data['purpose'] = second_match.group('purpose')
    if third_match:
        row_data['place'] = third_match.group('place')
        row_data['institution'] = third_match.group('institution')
    return row_data


def trabajos_dirigidos(data_extracted):
    first_extra_patter = re.compile(
        r'^Desde ?(?P<start_month>[\wáéíóúñÁÉÍÓÚÑ]+)? (?P<start_year>\d{4})? hasta ?(?P<end_month>[\wáéíóúñÁÉÍÓÚÑ]+)? ?(?P<end_year>\d{4})?, ?Tipo de orientación: ?(?P<orientation_type>.+)?'
    )
    second_extra_patter = re.compile(
        r'^Nombre del estudiante: ?(?P<student_names>.+)?, ?Programa académico: ?(?P<academic_program>.+)?'
    )
    third_extra_patter = re.compile(
        r'^Número de páginas: (?P<nro_pags>.+)?, ?Valoración: ?(?P<calification>.+)?, ?Institución: ?(?P<institution>.*)'
    )
    row_data = {}
    row_data['type'] = data_extracted[1].strip()
    row_data['title'] = data_extracted[2].strip(': ')
    first_extra = re.sub("[ \n]+", " ", data_extracted[3]).strip()
    second_extra = re.sub("[ \n]+", " ", data_extracted[4]).strip()
    third_extra = re.sub("[ \n]+", " ", data_extracted[5]).strip()
    row_data['authors'] = data_extracted[6].split(':')[1].strip()
    first_match = first_extra_patter.match(first_extra)
    second_match = second_extra_patter.match(second_extra)
    third_match = third_extra_patter.match(third_extra)
    if first_match:
        row_data['year'] = first_match.group('start_year')
        row_data['startYear'] = first_match.group('start_year')
        row_data['startMonth'] = first_match.group('start_month')
        row_data['endYear'] = first_match.group('end_year')
        row_data['endMonth'] = first_match.group('end_month')
        row_data['orientationType'] = first_match.group('orientation_type')
    if second_match:
        row_data['studentNames'] = second_match.group('student_names')
        row_data['academicProgram'] = second_match.group('academic_program')
    if third_match:
        row_data['nroPags'] = third_match.group('nro_pags')
        row_data['calification'] = third_match.group('calification')
        row_data['institution'] = third_match.group('institution')
    return row_data


def jurado_evaluadores_trabajos(data_extracted):
    first_extra_patter = re.compile(
        r'^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+)?, ?(?P<year>\d{4})?, ?Idioma: ?(?P<language>[\wáéíóúñÁÉÍÓÚÑ ]+)?, ?Medio de divulgación: ?(?P<media>[\wáéíóúñÁÉÍÓÚÑ ]+)?'
    )
    second_extra_patter = re.compile(
        r'^Sitio web: ?(?P<web>.+)?, ?Nombre del orientado: ?(?P<oriented_people>.+)?'
    )
    third_extra_patter = re.compile(
        r'^Programa académico: ?(?P<academic_program>.+)?, ?Institución: ?(?P<institution>.+)?'
    )
    row_data = {}
    row_data['type'] = data_extracted[1].strip()
    row_data['title'] = data_extracted[2].strip(': ')
    first_extra = re.sub("[ \n]+", " ", data_extracted[3]).strip()
    second_extra = re.sub("[ \n]+", " ", data_extracted[4]).strip()
    third_extra = re.sub("[ \n]+", " ", data_extracted[5]).strip()
    row_data['authors'] = data_extracted[6].split(':')[1].strip()
    first_match = first_extra_patter.match(first_extra)
    second_match = second_extra_patter.match(second_extra)
    third_match = third_extra_patter.match(third_extra)
    if first_match:
        row_data['country'] = first_match.group('country')
        row_data['year'] = first_match.group('year')
        row_data['language'] = first_match.group('language')
        row_data['media'] = first_match.group('media')
    if second_match:
        row_data['web'] = second_match.group('web')
        row_data['orientedPeople'] = second_match.group('oriented_people')
    if third_match:
        row_data['academicProgram'] = third_match.group('academic_program')
        row_data['institution'] = third_match.group('institution')
    return row_data


def participacion_comites_evalucacion(data_extracted):
    first_extra_patter = re.compile(
        r'^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+)?, ?(?P<year>\d{4})?, ?Sitio web: ?(?P<web>.+)?'
    )
    second_extra_patter = re.compile(
        r'^Medio de divulgación: ?(?P<media>.+)?, ?Institución: ?(?P<institution>.+)?'
    )
    row_data = {}
    row_data['type'] = data_extracted[1].strip()
    row_data['title'] = data_extracted[2].strip(': ')
    first_extra = re.sub("[ \n]+", " ", data_extracted[3]).strip()
    second_extra = re.sub("[ \n]+", " ", data_extracted[4]).strip()
    row_data['authors'] = data_extracted[5].split(':')[1].strip()
    first_match = first_extra_patter.match(first_extra)
    second_match = second_extra_patter.match(second_extra)
    if first_match:
        row_data['country'] = first_match.group('country')
        row_data['year'] = first_match.group('year')
        row_data['web'] = first_match.group('web')
    if second_match:
        row_data['media'] = second_match.group('media')
        row_data['institution'] = second_match.group('institution')
    return row_data


def demas_trabajos(data_extracted):
    extra_patter = re.compile(
        r'^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+)?, ?(?P<year>\d{4})?, ?Idioma: (?P<language>[\wáéíóúñÁÉÍÓÚÑ ]+)?, ?Medio de divulgación: ?(?P<media>.+)?'
    )
    row_data = {}
    row_data['type'] = data_extracted[1].strip()
    row_data['title'] = data_extracted[2].strip(': ')
    extra = re.sub("[ \n]+", " ", data_extracted[3]).strip()
    row_data['authors'] = data_extracted[4].split(':')[1].strip()
    match = extra_patter.match(extra)
    if match:
        row_data['country'] = match.group('country')
        row_data['year'] = match.group('year')
        row_data['language'] = match.group('language')
        row_data['media'] = match.group('media')
    return row_data


def proyectos(data_extracted):
    dates_patter = re.compile(
        r'^(?P<start_year>\d{4})?/(?P<start_month>\d+)? ?- ?(?P<end_year>\d{4})?/?(?P<end_month>\d+)?'
    )
    row_data = {}
    row_data['type'] = data_extracted[1].strip()
    row_data['title'] = data_extracted[2].strip(': ')
    if len(data_extracted) > 3:
        extra = re.sub("[ \n]+", " ", data_extracted[3]).strip()
        match = dates_patter.match(extra)
        if match:
            row_data['year'] = match.group('start_year')
            row_data['startYear'] = match.group('start_year')
            row_data['startMonth'] = match.group('start_month')
            row_data['endYear'] = match.group('end_year')
            row_data['endMonth'] = match.group('end_month')
    return row_data


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
    'Innovaciones en Procesos y Procedimientos':
    disenos_innovacion,
    'Plantas piloto':
    plantas_piloto_otros_productos,
    'Otros productos tecnológicos':
    plantas_piloto_otros_productos,
    'Prototipos':
    disenos_innovacion,
    'Regulaciones y Normas':
    regulaciones_normas,
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
    # missing
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
