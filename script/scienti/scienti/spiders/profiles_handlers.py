def parse_profile_table(table):
    name = table.xpath('tr[1]/td/strong/text()').extract_first()
    table_idx = 5 if name == 'Perfil de colaboración' else 2
    cols = table.xpath(
        "tr[{}]/td/table/tr[2]/td/strong/text()".format(table_idx)).extract()
    rows = table.xpath('tr[{}]/td/table/tr'.format(table_idx))[2:]
    profile_data = {}
    profile_data['profile_name'] = name
    rows_values = []
    for row in rows:
        values = row.xpath('td/text() | td/strong/text()').extract()
        values = list(filter(lambda v: not v == '\xa0', values))
        row_data = dict(zip(cols, values))
        rows_values.append(row_data)
    profile_data['rows_values'] = rows_values
    return profile_data