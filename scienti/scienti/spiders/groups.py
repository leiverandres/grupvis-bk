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
            yield {
                'id': group.css('td::text')[0].extract(),
                'name': group.css('td > a::text').extract_first(),
                'leader': group.css('td > a::text')[1].extract(),
                'category': group.css('td::text')[2].extract(),
                'clasifiedIn': group.css('td::text')[-1].extract(),
                'groupLink': group.css('td > a::attr(href)').extract_first()
            }
            groupLink = group.css('td > a::attr(href)').extract_first()
            for groupLink in group.css('td > a'):
                yield response.follow(
                    groupLink, callback=self.parse_single_group)

    def parse_single_group(self, response):
        """ Extract detailed groups information, including research products
        """
        from urllib.parse import urlparse
        parsedURL = urlparse(response.url)
        group = parsedURL.query.split('=')[-1]
        filename = 'groups_pages/group-%s.html' % group
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
