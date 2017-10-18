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
            data[field] = value.strip()

        avoid_header_query = 'tr > td:not([class="celdaEncabezado"])::text'
        instituciones_node = tablesSelector[1]
        data['Instituciones'] = clean_list(
            instituciones_node.css(avoid_header_query).extract())
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
                member_row.css(
                    ':first_child > a::text').extract_first().strip(),
                'Link del perfil':
                member_row.css(
                    ':first_child > a::attr(href)').extract_first().strip(),
                'Vinculación':
                member_row.css(
                    'td:nth-of-type(2)::text').extract_first().strip(),
                'Horas dedicación':
                member_row.css(
                    'td:nth-of_type(3)::text').extract_first().strip(),
                'Inicio - Fin Vinculación':
                member_row.css('td:nth-of_type(4)::text').extract_first()
                .strip()
            }
            data['Integrantes del grupo'].append(cur_member)
        yield data

    def extract_products(tablesList):
        pass