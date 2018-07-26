import scrapy
import re
import urllib.parse as parse
from scrapy import Request

from .constants import FIELDS_MAP, MISSING_GROUPS, SECTIONS
from .handlers import HANDLERS


class GroupsUTPSpider(scrapy.Spider):
    name = "research_groups"
    allow_domains = ["scienti.colciencias.gov.co"]
    base_url = 'http://scienti.colciencias.gov.co:8083/ciencia-war/busquedaGruposPorInstitucion.do?maxRows=100&all_grupos_ins_tr_=true&all_grupos_ins_mr_=100&all_grupos_ins_p_={}'
    total_pages = 7  # for pages of 100 items each

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
            # groups_qty = row.xpath('td[2]/a/*[1]/text()').extract_first()
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
                'scientiLink':
                group.xpath('td[3]/a/@href').extract_first(),
                'leader':
                group.xpath('td[4]/a/text()').extract_first(),
                'Category':
                group.xpath('td[7]/text()').extract_first().split(' ')[1]
                .strip(),
                'ClassifiedIn':
                group.xpath('td[8]/text()').extract_first(),
                'universityName':
                response.meta['universityName']
            }
            yield group_data
            ## TODO
            ## Get into each group page and scrape it all
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

    # def parse(self, response):
    #     """ Extract list of groups with basic information
    #     """
    #     query = "table#grupos > tbody > tr[id^='grupos_row']"
    #     for group in response.css(query):
    #         group_data = {
    #             'code':
    #             group.css('td::text')[0].extract(),
    #             'leader':
    #             group.css('td > a::text')[1].extract(),
    #             'classificationDate':
    #             group.css('td::text')[-1].extract(),
    #             'classification2017':
    #             group.css('td::text')[2].extract().split(' ')[1].strip()
    #         }
    #         group_link = group.css(
    #             'td > a[href*="visualiza/visualizagr"]::attr(href)'
    #         ).extract_first()

    #         yield response.follow(
    #             group_link,
    #             callback=self.parse_single_group,
    #             meta={'groupData': group_data})

    # for group in MISSING_GROUPS:
    #     group_data = {'code': group['code']}
    #     yield response.follow(
    #         group['link'],
    #         callback=self.parse_single_group,
    #         meta={
    #             'groupData': group_data
    #         })

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
            elif field == "Área de conocimiento":
                bigArea, area = map(lambda x: x.strip(), value.split('--'))
                data['bigKnowledgeArea'] = bigArea
                data['knowledgeArea'] = area
            else:
                try:
                    json_name = FIELDS_MAP[field]
                    data[json_name] = value.strip() if value else ''
                except KeyError:
                    pass
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
            title_query = './tr/td[@class = "celdaEncabezado"]/text()'
            table_title = table.xpath(title_query).extract_first().strip()
            if rows:
                for row in rows:
                    row_data = {}
                    row_data['category'] = table_title
                    approved_img = row.xpath(
                        './td[starts-with(@class, "celdas_")]/img')
                    row_data['isApproved'] = True if approved_img else False
                    row_data['type'] = row.xpath(
                        './td[@class = "celdas1" or @class = "celdas0"]/strong/text()'
                    ).extract_first()
                    info = row.xpath(
                        './td[@class = "celdas0" or @class = "celdas1"]/text() | ./td/strong/text()'
                    ).extract()
                    row_data['rawData'] = ' '.join(
                        map(lambda x: x.strip(), info))
                    ## Extra data
                    try:
                        extractor = HANDLERS[table_title]
                        result = extractor(info)
                        row_data.update(result)
                    except KeyError:
                        pass
                    products.append(row_data)
        return products