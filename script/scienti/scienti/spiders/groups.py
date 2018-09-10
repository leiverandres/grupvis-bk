import scrapy
import re
import urllib.parse as parse
from scrapy import Request

from .constants import FIELDS_MAP, MISSING_GROUPS, SECTIONS
from .handlers import HANDLERS


class GroupsUTPSpider(scrapy.Spider):
    '''
    '''
    name = "research_groups"
    allow_domains = ["scienti.colciencias.gov.co"]
    base_url = 'https://scienti.colciencias.gov.co:8083/ciencia-war/busquedaGruposPorInstitucion.do?maxRows=100&all_grupos_ins_tr_=true&all_grupos_ins_p_={}&all_grupos_ins_mr_=100'
    total_pages = 8  # calculated for pages of 100 items each
    codes_set = set()  # set to avoid scrapyin many times same page

    def start_requests(self):
        urls = [
            self.base_url.format(page)
            for page in range(1, self.total_pages + 1)
        ]
        for url in urls:
            yield Request(url, callback=self.parse_universities_list)

    def parse_universities_list(self, response):
        """
        """
        rows = response.xpath('//tr[contains(@id, "all_grupos_ins_row")]')
        for row in rows:
            university_name = row.xpath('td[1]/text()').extract_first()
            university_link = row.xpath('td[2]/a/@href').extract_first()
            #     # groups_qty = row.xpath('td[2]/a/*[1]/text()').extract_first()
            url_params = {
                'grupos_mr_': 100,
                'grupos_p_': 1,
                'grupos_tr_': True,
                'maxRows': 100
            }
            university_link += '&' + parse.urlencode(url_params)
            full_url = response.urljoin(university_link)
            yield Request(
                full_url,
                callback=self.parse_groups_list,
                meta={'universityName': university_name})

    def parse_groups_list(self, response):
        """
        """
        ## Get groups info in the current page
        groups = response.xpath('//tr[starts-with(@id, "grupos_row")]')
        for group in groups:
            group_data = {
                'code':
                group.xpath('td[2]/text()').extract_first(),
                'groupName':
                group.xpath('td[3]/a/text()').extract_first(),
                'gruplacURL':
                group.xpath('td[3]/a/@href').extract_first(),
                'leader':
                group.xpath('td[4]/a/text()').extract_first(),
                'category':
                group.xpath('td[7]/text()').extract_first().split(' ')[1]
                .strip(),
                'ClassifiedIn':
                group.xpath('td[8]/text()').extract_first(),
                'universityName':
                response.meta['universityName']
            }
            ## Get into each group page and scrape it all
            if not group_data['code'] in self.codes_set:
                self.codes_set.add(group_data['code'])
                yield Request(
                    group_data['gruplacURL'],
                    callback=self.parse_group_page,
                    meta={'group_data': group_data})
        ## Generate next page link and follow it
        next_button = response.xpath('//a/img[@alt="Página Siguiente"]')
        if next_button:
            parsed_url = parse.urlparse(response.request.url)
            query_params = parse.parse_qs(parsed_url.query)
            current_page = query_params['grupos_p_'][0]
            query_params['grupos_p_'][0] = int(current_page) + 1
            query_str = parse.urlencode(query_params, doseq=True)
            next_page_url = parsed_url.geturl().split('?')[0] + '?' + query_str
            yield Request(
                next_page_url,
                callback=self.parse_groups_list,
                meta={'universityName': response.meta['universityName']})

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

    def parse_group_page(self, response):
        """ Extract detailed groups information, including research products
        """
        # Recap data obtained before
        group_data = response.meta['group_data'].copy()
        tables = response.css("table")
        basic_data_table = tables[0]
        ## Take all info rows, except title of table
        rows_with_info = basic_data_table.css('tr')[1:]
        for info_row in rows_with_info:
            field = info_row.css('td.celdasTitulo::text').extract_first()
            link = info_row.css('td.celdas2 > a')
            value = ''
            if link:
                value = link.css('::text').extract_first()
            else:
                value = info_row.css('td.celdas2::text').extract_first()
            ## Custom cases
            if field == "Departamento - Ciudad":
                departament, city = map(lambda x: x.strip(), value.split('-'))
                group_data['departament'] = departament
                group_data['city'] = city
            elif field == "Área de conocimiento":
                bigArea, area = map(lambda x: x.strip(), value.split('--'))
                group_data['bigKnowledgeArea'] = bigArea
                group_data['knowledgeArea'] = area
            else:
                try:
                    json_name = FIELDS_MAP[field]
                    group_data[json_name] = value.strip() if value else ''
                except KeyError:
                    pass
        # SELECTORS
        avoid_header_query = 'tr > td:not([class="celdaEncabezado"])::text'
        instituciones_node = tables[1]
        plan_node = tables[2]
        lines_node = tables[3]
        sectores_node = tables[4]
        members_node = tables[5].css('tr')[2:]
        product_nodes = tables[6:]
        # EXTRACTION
        group_data['institutions'] = self.extract_with_css(
            instituciones_node, avoid_header_query, split_dash=True)
        group_data['strategicPlan'] = ''.join(
            self.extract_with_css(plan_node, avoid_header_query))
        group_data['researchLines'] = self.extract_with_css(
            lines_node, avoid_header_query, split_dash=True)
        group_data['applicationFields'] = self.extract_with_css(
            sectores_node, avoid_header_query, split_dash=True)
        group_data['members'] = self.extract_members(members_node)
        group_data['products'] = self.process_products(
            product_nodes, group_data['gruplacURL'])
        yield group_data

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

    def extract_product_data(self, row, table_name):
        '''
        This function is useful for transforming the html text before perform
        data extraction of each product
        '''
        data_as_str = row.extract()
        custom_tags = ['un', 'urbanaenlinea.go.to']
        for tag_name in custom_tags:
            opening_tag = '<' + tag_name + '>'
            closing_tag = '</' + tag_name + '>'
            if opening_tag in data_as_str:
                data_as_str = data_as_str.replace(opening_tag, '').replace(
                    closing_tag, '')
        data_node = scrapy.Selector(text=data_as_str)
        unprocessed_data = data_node.xpath(
            '//td[@class = "celdas0" or @class = "celdas1"]/text() | //td/strong/text()'
        ).extract()
        extractor = HANDLERS[table_name]
        estructured_data = extractor(unprocessed_data)
        return estructured_data

    def process_products(self, tables_list, gruplac_url):
        keyerror_msg = 'While scraping <{}>\nThis may due to missing handler especified for {} or an error in handler function'
        products = []
        for table in tables_list:
            product_table_name = table.xpath(
                './tr/td[@class = "celdaEncabezado"]/text()').extract_first(
                ).strip()
            if product_table_name == "Producción en arte, arquitectura y diseño":
                ## something special
                rows = table.xpath('tr')
                cur_product_category = product_table_name
                for row in rows:
                    is_heading = row.xpath('td[@class="celdaEncabezado"]')
                    if is_heading:
                        cur_product_category = is_heading.xpath(
                            'text()').extract_first()
                    else:
                        row_data = {
                            'category': product_table_name,
                            'type': cur_product_category
                        }
                        try:
                            processed_data = self.extract_product_data(
                                row, cur_product_category)
                            row_data['rawData'] = ' '.join(
                                map(lambda x: x.strip(), processed_data))
                            row_data.update(processed_data)
                            products.append(row_data)
                        except KeyError:
                            self.logger.error(
                                keyerror_msg.format(gruplac_url,
                                                    cur_product_category),
                                exc_info=True)
            else:
                valid_rows = table.xpath(
                    './tr[td[@class != "celdaEncabezado"]]')
                if valid_rows:
                    for row_idx, row in enumerate(valid_rows):
                        row_data = {
                            'category':
                            product_table_name,
                            'type':
                            row.xpath(
                                './td[@class = "celdas1" or @class = "celdas0"]/strong/text()'
                            ).extract_first()
                        }
                        approved_img = row.xpath(
                            './td[starts-with(@class, "celdas_")]/img')
                        row_data[
                            'isApproved'] = True if approved_img else False
                        try:
                            processed_data = self.extract_product_data(
                                row, product_table_name)
                            row_data['rawData'] = ' '.join(
                                map(lambda x: x.strip(), processed_data))
                            row_data.update(processed_data)
                            products.append(row_data)
                        except KeyError:
                            self.logger.error(
                                keyerror_msg.format(gruplac_url,
                                                    product_table_name),
                                exec_info=True)
                        except IndexError as err:
                            self.logger.error(
                                "While scraping <{}>\n"
                                "IndexError: {}. This happend while processing row {}, of category \"{}\"\n"
                                "... Item Skipped".format(
                                    gruplac_url, err, row_idx + 1,
                                    product_table_name))
        return products

    def closed(self, reason):
        self.logger.info('unique codes found: {}'.format(
            self.codes_set.__len__()))
