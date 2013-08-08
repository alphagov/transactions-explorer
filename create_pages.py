#!/usr/bin/env python
import os
from distutils import dir_util

from jinja2 import Environment, FileSystemLoader

import unicodecsv
from lib.filesystem import create_directory
from lib.filters import number_as_grouped_number, number_as_financial_magnitude, number_as_magnitude, number_as_percentage, number_as_percentage_change
from lib.service import Service, latest_quarter, sorted_ignoring_empty_values, total_transaction_volume
from lib.slugify import slugify

jinja = Environment(
    loader=FileSystemLoader(searchpath='templates', encoding='utf-8'),
    trim_blocks=True,
    lstrip_blocks=True,
    extensions=['jinja2.ext.with_']
)

jinja.globals['STATIC_HOST'] = 'https://assets.digital.cabinet-office.gov.uk/static'
jinja.globals['EXPLORER_HOST'] = ''

jinja.filters['as_magnitude'] = number_as_magnitude
jinja.filters['as_financial_magnitude'] = number_as_financial_magnitude
jinja.filters['as_percentage'] = number_as_percentage
jinja.filters['as_percentage_change'] = number_as_percentage_change
jinja.filters['as_grouped_number'] = number_as_grouped_number
jinja.filters['slugify'] = slugify

SERVICES_DATA = 'data/services.csv'
OUTPUT_DIR = 'output'

data = open(SERVICES_DATA)
reader = unicodecsv.DictReader(data)

services = [Service(details=row) for row in reader]
high_volume_services = [service for service in services if service.high_volume]
latest_quarter = latest_quarter(high_volume_services)
departments = set(s.department for s in services)


def render(template_name, out, vars):
    template = jinja.get_template(template_name)
    page = template.render(**vars)
    output_path = os.path.join(OUTPUT_DIR, out)
    create_directory(os.path.dirname(output_path))
    with open(output_path, 'w') as output:
        output.write(page.encode('utf8'))


if __name__ == "__main__":
    render("about-the-data.html", "aboutData.html", {})
    render("home.html", "home.html", {
        'departments_count': len(departments),
        'services_count': len(services),
        'total_transactions': total_transaction_volume(services)
    })

    for service in high_volume_services:
        print service.name

        render('service_detail.html',
               out=service.link,
               vars={"service": service})


    sort_orders = [
        ("by-name", lambda service: service.name_of_service),
        ("by-department", lambda service: service.abbr),
        ("by-total-cost", lambda service: service.most_recent_kpis['cost']),
        ("by-cost-per-transaction", lambda service: service.most_recent_kpis['cost_per_number']),
        ("by-digital-takeup", lambda service: service.most_recent_kpis['takeup']),
        ("by-transactions-per-year", lambda service: service.most_recent_kpis['volume_num']),
    ]

    for sort_order, key in sort_orders:
        for direction in ['ascending', 'descending']:
            reverse = (direction == 'descending')
            variables = {
                'services': sorted_ignoring_empty_values(high_volume_services,
                                                         key=key, reverse=reverse),
                'latest_quarter': latest_quarter,
                'current_sort': {
                    'order': sort_order,
                    'direction': direction
                },
            }
            render('high_volume_services.html',
                   out="high-volume-services/%s/%s.html" % (sort_order, direction),
                   vars=variables)
    
    # Copy the assets folder entirely, as well
    dir_util.copy_tree('assets', '%s/assets' % OUTPUT_DIR)
