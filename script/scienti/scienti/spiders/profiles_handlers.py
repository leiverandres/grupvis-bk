def process_new_knowledge(table):
    name = table.xpath('td/table/tr[1]/td/strong/text()').extract_first()
    values_table = table.xpath('td/table/tr[2]//table')
    cols = table.xpath(
        "tr[2]//td[@class = 'encabezado']/strong/text()").extract()
    rows = table.xpath("tr")[2:]

    for row in rows:
        values = rows[0].xpath('td/text() | td/strong/text()').extract()
        row_data = dict(zip(cols, values))
