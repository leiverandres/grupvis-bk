import re


def articulos_publicados(data_extracted):
    extra_patter = re.compile(
        '^(?P<country>[\wáéíóúñÁÉÍÓÚÑ ]+),[ ]*(?P<publisher>[\wáéíóúñÁÉÍÓÚÑ:.\-()\'"_ ]+)[ ]*ISSN: (?P<issn>\d{4}-\d{3}[\dx00X]), (?P<year>\d{4})?[ ]*vol: ?(?P<vol>([aA][Ññ][oO] ?)?(\d+|N/A|n/a|[CMDIXLV]+))?[ ]*fasc: (?P<fasc>(\d+|[Nn]/?7?[Aa]))?[ ]*págs: (?P<pags>([\d\w]+|N/A|n/a)?[- ]*([\d\w]+|N/A|n/a)?)?,'
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


HANDLERS = {
    'Artículos publicados': articulos_publicados,
    'Libros publicados': libros_publicados,
    'Capítulos de libro publicados': capitulos_libro_publicado
}
