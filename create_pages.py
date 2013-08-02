#!/usr/bin/env python

import unicodecsv
import re

from lib.service import Service
from lib.slugify import slugify

from jinja2 import Environment, FileSystemLoader

jinja = Environment(
    loader=FileSystemLoader(searchpath='templates', encoding='utf-8'),
    trim_blocks=True,
    lstrip_blocks=True,
)

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
            'output/serviceDetails/',
            slugify( '%s-%s' % (service.abbr, service.name) ),
        )
        output = open(output_filename, 'w')
        output.write( page.encode('utf8') )
