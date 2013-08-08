#!/usr/bin/env python

from distutils import dir_util

import unicodecsv
from lib import templates

from lib.service import Service, latest_quarter, sorted_ignoring_empty_values
from lib.templates import render


SERVICES_DATA = 'data/services.csv'
OUTPUT_DIR = 'output'

templates.output_dir = OUTPUT_DIR

data = open(SERVICES_DATA)
reader = unicodecsv.DictReader(data)

services = [Service(details=row) for row in reader]
high_volume_services = [service for service in services if service.high_volume]
latest_quarter = latest_quarter(high_volume_services)


for service in high_volume_services:
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

"""Copy the assets folder entirely, as well"""
dir_util.copy_tree('assets', '%s/assets' % OUTPUT_DIR)

