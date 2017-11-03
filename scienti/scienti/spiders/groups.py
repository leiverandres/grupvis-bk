import scrapy
from .constants import FIELDS_MAP, MISSING_GROUPS, SECTIONS


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

        for group in MISSING_GROUPS:
            groupData = {'code': group['code']}
            yield response.follow(
                group['link'],
                callback=self.parse_single_group,
                meta={'groupData': groupData})

    def extract_with_css(self,
                         initial_selector,
                         query,
                         extract_first=False,
                         split_dash=False):
        if extract_first:
            return initial_selector.css(query).extract_first().strip()
        else:
            if split_dash:
                return list(
                    map(lambda item: item.split('-')[1].strip(),
                        initial_selector.css(query).extract()))
            else:
                return list(
                    map(lambda item: item.strip(),
                        initial_selector.css(query).extract()))

    def parse_single_group(self, response):
        """ Extract detailed groups information, including research products
        """
        group_name = response.xpath(
            '//span[@class="celdaEncabezado"]/text()').extract_first()
        data = {'grouplacURL': response.url, 'name': group_name}

        # merging data with the data got in parser
        data.update(response.meta['groupData'])
        tables_selector = response.css("table")
        basic_data = tables_selector[0]
        for row in basic_data.css('tr')[1:]:
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

        # SELECTORS
        avoid_header_query = 'tr > td:not([class="celdaEncabezado"])::text'
        instituciones_node = tables_selector[1]
        plan_node = tables_selector[2]
        lines_node = tables_selector[3]
        sectores_node = tables_selector[4]
        members_node = tables_selector[5].css('tr')[2:]
        product_nodes = tables_selector[6:]
        # EXTRACTION
        data['institutions'] = self.extract_with_css(
            instituciones_node, avoid_header_query, split_dash=True)
        data['strategicPlan'] = ''.join(
            self.extract_with_css(plan_node, avoid_header_query))
        data['researchLines'] = self.extract_with_css(
            lines_node, avoid_header_query, split_dash=True)
        data['applicationFields'] = self.extract_with_css(
            sectores_node, avoid_header_query, split_dash=True)
        data['members'] = self.extract_members(members_node)
        data['products'] = self.extract_products(product_nodes)
        yield data

    def extract_members(self, member_list):
        members = []
        for member_row in member_list:
            date = self.extract_with_css(member_row, 'td:nth-of_type(4)::text',
                                         True)
            cur_member_data = {
                'name':
                self.extract_with_css(member_row, ':first_child > a::text',
                                      True),
                'profileURL':
                self.extract_with_css(member_row,
                                      ':first_child > a::attr(href)', True),
                'rol':
                self.extract_with_css(member_row, 'td:nth-of-type(2)::text',
                                      True),
                'dedicatedHours':
                self.extract_with_css(member_row, 'td:nth-of_type(3)::text',
                                      True),
                'startingDate':
                date.split('-')[0].strip(),
                'endingDate':
                date.split('-')[1].strip()
            }
            members.append(cur_member_data)
        return members

    def extract_products(self, tablesList):
        products = []
        for table in tablesList:
            valid_rows_query = './tr[td[@class != "celdaEncabezado"]]'
            rows = table.xpath(valid_rows_query)
            table_title = self.extract_with_css(
                table, 'tr > td.celdaEncabezado::text', True)
            if rows:
                for row in rows:
                    row_data = {}
                    row_data['category'] = table_title
                    approved_img = row.xpath(
                        './td[starts-with(@class, "celdas_")]/img')
                    row_data['isApproved'] = True if approved_img else False
                    row_data['type'] = row.xpath(
                        './td[starts-with(@class, "celdas1")]/strong/text()'
                    ).extract_first()
                    info = list(
                        map(lambda item: item.strip(),
                            row.xpath(
                                './td[starts-with(@class, "celdas1")]/text()')
                            .extract()[1:]))
                    row_data['description'] = ' '.join(info)
                    products.append(row_data)
        return products


'''

p = re.compile(r'^\d+\.- (?P<type>[\wáéíóúñ ]+):(?P<name>[\wáéíóúñ ]+)\n([\w]+),')
m = p.search(st)
m.group('type')
'''