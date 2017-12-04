import re


def articulos_publicados(data_extracted):
    extra_patter = re.compile(
        '^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+),[ ]*(?P<publisher>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_ ]+)[ ]*ISSN: (?P<issn>\d{4}-\d{3}[\dx00X]|\d+), (?P<year>\d{4})?[ ]*vol: ?(?P<vol>([aA][Ññ][oO] ?)?(\d+|N/A|n/a|[CMDIXLV]+))?[ ]*fasc: (?P<fasc>(\d+|[Nn]/?7?[Aa]))?[ ]*págs: (?P<pags>([\d\w]+|N/A|n/a)?[- ]*([\d\w]+|N/A|n/a)?)?,?'
    )
    row_data = {}
    row_data['type'] = data_extracted[1].strip(': ')
    row_data['title'] = data_extracted[2].strip()
    extra = data_extracted[3].strip()
    row_data['doi'] = data_extracted[5].strip()
    row_data['authors'] = data_extracted[6].strip().split(':')[1]

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
        '^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+), ?(?P<year>\d{4})?, ?ISBN: (?P<isbn>[\d\- ]+) ?vol: (?P<vol>([aA][Ññ][oO] ?)?(\d+|N/A|n/a|[CMDIXLV]+))? ?págs: ?(?P<pags>([\d\w]+|N/A|n/a)?[- ]*([\d\w]+|N/A|n/a)?)?, ?Ed. ?(?P<editorial>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_ ]+)'
    )
    row_data = {}
    row_data['type'] = data_extracted[1].strip()
    row_data['title'] = data_extracted[2].strip(': ')
    row_data['authors'] = data_extracted[4].strip().split(':')[1]
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
        '^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+), ?(?P<year>\d{4})?, ?(?P<book>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_ ]+), ?ISBN: (?P<isbn>[\d\- ]+), ?Vol. (?P<vol>([aA][Ññ][oO] ?)?(\d+|N/A|n/a|[CMDIXLV]+))?, ?págs: ?(?P<pags>([\d\w]+|N/A|n/a)?[- ]*([\d\w]+|N/A|n/a)?)?, ?Ed. ?(?P<editorial>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_ ]+)'
    )
    row_data = {}
    row_data['type'] = data_extracted[1].strip()
    row_data['title'] = data_extracted[2].strip(': ')
    row_data['authors'] = data_extracted[4].strip().split(':')[1]
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
        '^(?P<year>\d{4}), Nro. Paginas: ?(?P<nro_pags>\d+)?, Instituciones participantes: ?(?P<institutions>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_,; ]+)?, URL: ?(?P<url>[\w:/.?=#$%-_]+)?, DOI: ?(?P<doi>[\w:/.?=#$%-]+)?'
    )
    row_data = {}
    row_data['type'] = data_extracted[1].strip()
    row_data['title'] = data_extracted[2].strip(': ')
    row_data['authors'] = data_extracted[4].strip().split(':')[1]
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
        '^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+), ?(?P<year>\d{4})?,.*')
    row_data = {}
    row_data['type'] = data_extracted[1].strip()
    row_data['title'] = data_extracted[2].strip(': ')
    row_data['authors'] = data_extracted[4].strip().split(':')[1]
    extra = data_extracted[3].strip()
    extra = re.sub("[ \n]+", " ", extra)
    match = extra_patter.match(extra)
    if match:
        row_data['country'] = match.group('country')
        row_data['year'] = match.group('year')
    return row_data


def traducciones(data_extracted):
    extra_patter = re.compile(
        '^(?P<year>\d{4}), ?Revista: ?(?P<magazine>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_ ]+)? ?ISSN ?(?P<issn>\d{4}-\d{3}[\dx00X]|\d+)?, ?Libro: ?(?P<book>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_ ]+)? ?ISBN ?(?P<isbn>[\d\- ]+), ?Medio de divulgación: ?(?P<media>[\wáéíóúñÁÉÍÓÚÑ ]+)'
    )
    row_data = {}
    row_data['type'] = data_extracted[1].strip()
    row_data['title'] = data_extracted[2].strip(': ')
    languages = data_extracted[4].strip(',\n ').split(',')
    row_data['originallanguage'] = languages[0].split(':')[1].strip()
    row_data['translationLanguage'] = languages[1].split(':')[1].strip()
    row_data['authors'] = data_extracted[6].strip().split(':')[1]
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


HANDLERS = {
    'Artículos publicados': articulos_publicados,
    'Libros publicados': libros_publicados,
    'Capítulos de libro publicados': capitulos_libro_publicado,
    'Documentos de trabajo': documentos_trabajo,
    'Otra publicación divulgativa': otra_publicacion_divulgativa,
    'Otros artículos publicados': articulos_publicados,
    'Otros Libros publicados': libros_publicados,
    'Traducciones': traducciones
}
