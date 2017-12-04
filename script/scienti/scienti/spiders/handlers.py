import re


def articulos_publicados(data_extracted):
    extra_patter = re.compile(
        r'^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+),[ ]*(?P<publisher>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_ ]+)[ ]*ISSN: (?P<issn>\d{4}-\d{3}[\dx00X]|\d+), (?P<year>\d{4})?[ ]*vol: ?(?P<vol>([aA][Ññ][oO] ?)?(\d+|N/A|n/a|[CMDIXLV]+))?[ ]*fasc: (?P<fasc>(\d+|[Nn]/?7?[Aa]))?[ ]*págs: (?P<pags>([\d\w]+|N/A|n/a)?[- ]*([\d\w]+|N/A|n/a)?)?,?'
    )
    row_data = {}
    row_data['type'] = data_extracted[1].strip(': ')
    row_data['title'] = data_extracted[2].strip()
    extra = data_extracted[3].strip()
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
    extra = data_extracted[3].strip()
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
    extra = data_extracted[3].strip()

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
    extra = data_extracted[3].strip()
    extra = re.sub("[ \n]+", " ", extra)

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
    extra = data_extracted[3].strip()
    extra = re.sub("[ \n]+", " ", extra)
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
    first_extra = re.sub("[ \n]+", " ", data_extracted[3].strip())
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
    extra_patter = re.compile(
        r'^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+)?, ?(?P<publisher>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_ ]+)? ?ISSN: (?P<issn>\d{4}-\d{3}[\dx00X]|\d+)?, ?(?P<year>\d{4})? ?vol: ?(?P<vol>([aA][Ññ][oO] ?)?(\d+|N/A|n/a|[CMDIXLV]+))? ?fasc: ?(?P<fasc>(\d+|[Nn]/?7?[Aa]))? ?págs: (?P<pags>([\d\w]+|N/A|n/a)?[- ]*([\d\w]+|N/A|n/a)?)?,?'
    )
    row_data = {}
    row_data['type'] = data_extracted[1].strip(': ')
    row_data['title'] = data_extracted[2].strip()
    row_data['authors'] = data_extracted[4].split(':')[1].strip(', ')
    extra = data_extracted[3].strip()
    extra = re.sub("[ \n]+", " ", extra)

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
    extra = data_extracted[3].strip()
    extra = re.sub("[ \n]+", " ", extra)
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
    extra = data_extracted[3].strip()
    extra = re.sub("[ \n]+", " ", extra)
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
    extra = data_extracted[3].strip()
    extra = re.sub("[ \n]+", " ", extra)
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
    extra = data_extracted[3].strip()
    extra = re.sub("[ \n]+", " ", extra)
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
    extra = data_extracted[3].strip()
    extra = re.sub("[ \n]+", " ", extra)
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
    extra = data_extracted[3].strip()
    extra = re.sub("[ \n]+", " ", extra)
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
    extra = data_extracted[3].strip()
    extra = re.sub("[ \n]+", " ", extra)
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
    extra = data_extracted[3].strip()
    extra = re.sub("[ \n]+", " ", extra)
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
    extra = data_extracted[3].strip()
    extra = re.sub("[ \n]+", " ", extra)
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
        row_data['start_date'] = match.group('start_date')
        row_data['end_date'] = match.group('end_date')
    return row_data


HANDLERS = {
    'Artículos publicados': articulos_publicados,
    'Libros publicados': libros_publicados,
    'Capítulos de libro publicados': capitulos_libro_publicado,
    'Documentos de trabajo': documentos_trabajo,
    'Otra publicación divulgativa': otra_publicacion_divulgativa,
    'Otros artículos publicados': otros_articulos_publicados,
    'Otros Libros publicados': libros_publicados,
    'Traducciones': traducciones,
    'Cartas, mapas o similares': cartas_mapas_similares,
    'Consultorías científico tecnológicas e Informes técnicos': consultorias,
    'Diseños industriales': disenos_innovacion,
    'Innovaciones en Procesos y Procedimientos': disenos_innovacion,
    'Plantas piloto': plantas_piloto_otros_productos,
    'Otros productos tecnológicos': plantas_piloto_otros_productos,
    'Prototipos': disenos_innovacion,
    'Regulaciones y Normas': regulaciones_normas,
    'Signos distintivos': signos_distintivos,
    'Softwares': softwares,
    'Empresas de base tecnológica': empresas_base_tecnologica,
    'Ediciones': ediciones,
    'Eventos Científicos': eventos_cientificos,
    'Informes de investigación': informes_investigacion,
    'Redes de Conocimiento Especializado': redes_conocimiento
}
