import scrapy


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
                # 'category': group.css('td::text')[2].extract(), // is in basic info
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
        # tablesNames = response.css('table td.celdaEncabezado::text').extract()
        basicData = response.css("table")[0]
        # merging data with the data got in parser
        data = {'url': response.url}
        data.update(response.meta['groupData'])
        for row in basicData.css('tr')[1:]:
            field = row.css('td.celdasTitulo::text').extract_first()
            link = row.css('td.celdas2 > a')
            value = ''
            if link:
                value = link.css('::text').extract_first()
            else:
                value = row.css('td.celdas2::text').extract_first()
            data[field] = value.strip()
        yield data
