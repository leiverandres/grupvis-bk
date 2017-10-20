import scrapy

SECTIONS = [
    'PRODUCCIÓN BIBLIOGRÁFICA', 'PRODUCCIÓN TÉCNICA Y TECNOLÓGICA',
    'APROPIACIÓN SOCIAL Y CIRCULACIÓN DEL CONOCIMIENTO',
    'ACTIVIDADES DE FORMACIÓN', 'ACTIVIDADES COMO EVALUADOR'
]


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
                'Código del grupo': group.css('td::text')[0].extract(),
                'Nombre del grupo': group.css('td > a::text').extract_first(),
                'Líder': group.css('td > a::text')[1].extract(),
                'Clasificado en': group.css('td::text')[-1].extract()
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
                map(lambda item: item.strip(),
                    initial_selector.css(query).extract()))

    def parse_single_group(self, response):
        """ Extract detailed groups information, including research products
        """
        data = {'url': response.url}
        # merging data with the data got in parser
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
            data[field] = value.strip() if value else ''

        avoid_header_query = 'tr > td:not([class="celdaEncabezado"])::text'
        instituciones_node = tablesSelector[1]
        data['Instituciones'] = '; '.join(
            clean_list(instituciones_node.css(avoid_header_query).extract()))
        plan = tablesSelector[2]
        data['Plan Estratégico'] = ''.join(
            clean_list(plan.css(avoid_header_query).extract()))
        lines = tablesSelector[3]
        data['Líneas de investigación declaradas por el grupo'] = clean_list(
            lines.css(avoid_header_query).extract())
        sectores = tablesSelector[4]
        data['Sectores de aplicación'] = clean_list(
            sectores.css(avoid_header_query).extract())
        members = tablesSelector[5]
        data['Integrantes del grupo'] = []
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
        data['Integrantes del grupo'].append(cur_member)
        data['Productos'] = self.extract_products(tablesSelector[6:])
        yield data

    def extract_products(self, tablesList):
        products = {}
        for table in tablesList:
            valid_rows_query = './tr[td[@class != "celdaEncabezado"]]'
            rows = table.xpath(valid_rows_query)
            table_title = self.extract_with_css(
                table, 'tr > td.celdaEncabezado::text', True)
            # table_title = table.css(
            #     'tr > td.celdaEncabezado::text').extract_first()
            products[table_title] = []
            if rows:
                for row in rows:
                    row_data = {}
                    approved_img = row.xpath(
                        './td[starts-with(@class, "celdas_")]/img')
                    row_data['Avalado'] = True if approved_img else False
                    row_data['Tipo'] = row.xpath(
                        './td[starts-with(@class, "celdas1")]/strong/text()'
                    ).extract_first()
                    info = row.xpath(
                        './td[starts-with(@class, "celdas1")]/text()').extract(
                        )[1:]
                    row_data['Descripción'] = ' '.join(info[1:])
        return products