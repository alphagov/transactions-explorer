#!/usr/bin/env python

import unicodecsv
import re

from lib.filters import number_as_grouped_number, number_as_financial_magnitude, number_as_magnitude, number_as_percentage, number_as_percentage_change, period_as_text
from lib.service import Service
from lib.slugify import slugify

from jinja2 import Environment, FileSystemLoader

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
for row in reader:
    service = Service(details=row)
    print service.name
    
    if service.high_volume:
        template = jinja.get_template('service_detail.html')
        page = template.render(service=service)
        
        output_filename = '%s/%s.html' % (
            'output/service-details/',
            slugify( '%s-%s' % (service.abbr, service.name) ),
        )
        output = open(output_filename, 'w')
        output.write( page.encode('utf8') )
