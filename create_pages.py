#!/usr/bin/env python
import os

import unicodecsv
from jinja2 import Environment, FileSystemLoader

from lib.filters import number_as_grouped_number, number_as_financial_magnitude, number_as_magnitude, number_as_percentage, number_as_percentage_change, period_as_text
from lib.service import Service
from lib.slugify import slugify

jinja = Environment(
    loader=FileSystemLoader(searchpath='templates', encoding='utf-8'),
    trim_blocks=True,
    lstrip_blocks=True,
    extensions=['jinja2.ext.with_'],
)

jinja.filters['as_magnitude'] = number_as_magnitude
jinja.filters['as_financial_magnitude'] = number_as_financial_magnitude
jinja.filters['as_percentage'] = number_as_percentage
jinja.filters['as_percentage_change'] = number_as_percentage_change
jinja.filters['as_grouped_number'] = number_as_grouped_number
jinja.filters['period_as_text'] = period_as_text
jinja.filters['slugify'] = slugify

SERVICES_DATA = 'data/services.csv'

data = open(SERVICES_DATA)
reader = unicodecsv.DictReader(data)

services = [Service(details=row) for row in reader]
high_volume_services = [service for service in services if service.high_volume]


def render(template_name, out, vars):
    template = jinja.get_template(template_name)
    page = template.render(**vars)
    output_path = os.path.join('output', out)
    with open(output_path, 'w') as output:
        output.write(page.encode('utf8'))


for service in high_volume_services:
    print service.name

    output_filename = '%s/%s.html' % ('service-details/', service.slug)

    render('service_detail.html',
           out=output_filename,
           vars={"service": service})

print "High Volume Transactions"

render('high_volume_transactions.html',
       out='high-volume-transactions.html',
       vars={'services': high_volume_services})
