import scrapy

SECTIONS = [
    'PRODUCCIÓN BIBLIOGRÁFICA', 'PRODUCCIÓN TÉCNICA Y TECNOLÓGICA',
    'APROPIACIÓN SOCIAL Y CIRCULACIÓN DEL CONOCIMIENTO',
    'ACTIVIDADES DE FORMACIÓN', 'ACTIVIDADES COMO EVALUADOR'
]

FIELDS_MAP = {
    'Año y mes de formación':
    'foundationDate',
    'Líder':
    'leader',
    '¿La información de este grupo se ha certificado? ':
    'certified',
    'Página web':
    'website',
    'E-mail':
    'email',
    'Clasificación':
    'clasification',
    'Área de conocimiento':
    'knowledgeArea',
    'Programa nacional de ciencia y tecnología':
    'nationalProgramOfScienceAndTechnology',
    'Programa nacional de ciencia y tecnología (secundario)':
    'secondaryNationalProgramOfScienceAndTechnology'
}


def clean_list(dirty_list):
    ''' Remove spacing characters from every list item
    '''
    new_list = list(map(lambda x: x.strip(), dirty_list))
    return new_list


class GroupsUTPSpider(scrapy.Spider):
    name = "utp_research_groups"
    # storing-the-scraped-data
    start_urls = [
        "http://scienti.colciencias.gov.co:8083/ciencia-war/busquedaGrupoXInstitucionGrupos.do?codInst=011600000880&sglPais=&sgDepartamento=&maxRows=100&grupos_tr_=true&grupos_p_=1&grupos_mr_=100"
    ]

    def parse(self, response):
        """ Extract list of groups with basic information
        """
        query = "table#grupos > tbody > tr[id^='grupos_row']"
        for group in response.css(query):
            groupData = {
                'code': group.css('td::text')[0].extract(),
                'name': group.css('td > a::text').extract_first(),
                'leader': group.css('td > a::text')[1].extract(),
                'classificationDate': group.css('td::text')[-1].extract()
            }
            groupLink = group.css(
                'td > a[href*="visualiza/visualizagr"]::attr(href)'
            ).extract_first()

            yield response.follow(
                groupLink,
                callback=self.parse_single_group,
                meta={'groupData': groupData})

    def extract_with_css(self, initial_selector, query, extract_first=False):
        if extract_first:
            return initial_selector.css(query).extract_first().strip()
        else:
            return list(
                map(lambda item: item.split('-')[1].strip(),
                    initial_selector.css(query).extract()))

    def parse_single_group(self, response):
        """ Extract detailed groups information, including research products
        """
        data = {'grouplacURL': response.url}
        # merging data with the data one got in parser
        data.update(response.meta['groupData'])
        tablesSelector = response.css("table")
        basicData = tablesSelector[0]
        for row in basicData.css('tr')[1:]:
            field = row.css('td.celdasTitulo::text').extract_first()
            link = row.css('td.celdas2 > a')
            value = ''
            if link:
                value = link.css('::text').extract_first()
            else:
                value = row.css('td.celdas2::text').extract_first()
            ## Custom cases
            if field == "Departamento - Ciudad":
                departament, city = map(lambda x: x.strip(), value.split('-'))
                data['departament'] = departament
                data['city'] = city
            else:
                json_name = FIELDS_MAP[field]
                data[json_name] = value.strip() if value else ''

        avoid_header_query = 'tr > td:not([class="celdaEncabezado"])::text'
        instituciones_node = tablesSelector[1]
        data['Instituciones'] = 
            extract_with_css(instituciones_node, avoid_header_query)
        plan = tablesSelector[2]
        data['Plan Estratégico'] = ''.join(
            clean_list(plan.css(avoid_header_query).extract()))
        lines = tablesSelector[3]
        data[
            'Líneas de investigación declaradas por el grupo'] = extract_with_css(
                lines, avoid_header_query)
        sectores = tablesSelector[4]
        data['Sectores de aplicación'] = clean_list(
            sectores.css(avoid_header_query).extract())
        members = tablesSelector[5]
        data['members'] = []
        for member_row in members.css('tr')[2:]:
            cur_member = {
                'Nombre':
                self.extract_with_css(member_row, ':first_child > a::text',
                                      True),
                'Link del perfil':
                self.extract_with_css(member_row,
                                      ':first_child > a::attr(href)', True),
                'Vinculación':
                self.extract_with_css(member_row, 'td:nth-of-type(2)::text',
                                      True),
                'Horas dedicación':
                self.extract_with_css(member_row, 'td:nth-of_type(3)::text',
                                      True),
                'Inicio - Fin Vinculación':
                self.extract_with_css(member_row, 'td:nth-of_type(4)::text',
                                      True)
            }
        data['members'].append(cur_member)
        data['products'] = self.extract_products(tablesSelector[6:])
        yield data

    def extract_products(self, tablesList):
        products = {}
        for table in tablesList:
            valid_rows_query = './tr[td[@class != "celdaEncabezado"]]'
            rows = table.xpath(valid_rows_query)
            table_title = self.extract_with_css(
                table, 'tr > td.celdaEncabezado::text', True)
            if rows:
                products[table_title] = []
                for row in rows:
                    row_data = {}
                    approved_img = row.xpath(
                        './td[starts-with(@class, "celdas_")]/img')
                    row_data['Avalado'] = True if approved_img else False
                    row_data['Tipo'] = row.xpath(
                        './td[starts-with(@class, "celdas1")]/strong/text()'
                    ).extract_first()
                    info = list(
                        map(lambda item: item.strip(),
                            row.xpath(
                                './td[starts-with(@class, "celdas1")]/text()')
                            .extract()[1:]))
                    row_data['Descripción'] = ' '.join(info)
                    products[table_title].append(row_data)
        return products