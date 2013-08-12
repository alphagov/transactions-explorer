def table_from(rows):
    def cells(row):
        name = [row.find_by_css('th').text]
        values = map(lambda elem: elem.text, row.find_by_css('td'))
        return name + values

    return map(cells, rows)
