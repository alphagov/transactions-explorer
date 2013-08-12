#!/usr/bin/env python
import sys
from distutils import dir_util

import unicodecsv

from lib.service import Service, latest_quarter, sorted_ignoring_empty_values, Department

from lib import templates
from lib.csv import map_services_to_csv_data

from lib.service import Service, latest_quarter, sorted_ignoring_empty_values,\
    total_transaction_volume
from lib.templates import render, render_csv


SERVICES_DATA = 'data/services.csv'
OUTPUT_DIR = 'output'

templates.output_dir = OUTPUT_DIR

input = sys.argv[1] if len(sys.argv) > 1 else SERVICES_DATA

data = open(input)

reader = unicodecsv.DictReader(data)

services = [Service(details=row) for row in reader]
high_volume_services = [service for service in services if service.high_volume]
latest_quarter = latest_quarter(high_volume_services)

departments = set(s.department for s in services)

def generate_sorted_pages(items, page_name, sort_orders, extra_variables={}):
    for sort_order, key in sort_orders:
        for direction in ['ascending', 'descending']:
            reverse = (direction == 'descending')
            variables = dict({
                'items': sorted_ignoring_empty_values(items, key=key,
                                                      reverse=reverse),
                'current_sort': {
                    'order': sort_order,
                    'direction': direction
                },
            }.items() + extra_variables.items())
            render('%s.html' % page_name,
                   out="%s/%s/%s.html" % (page_name, sort_order, direction),
                   vars=variables)


if __name__ == "__main__":
    render("about-the-data.html", "about-data.html", {})
    render("home.html", "home.html", {
        'departments_count': len(departments),
        'services_count': len(services),
        'total_transactions': total_transaction_volume(services)
    })
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
    generate_sorted_pages(high_volume_services, 'high-volume-services',
                          sort_orders, {'latest_quarter': latest_quarter})


    departments = Department.from_services(services)
    department_sort_orders = [
        ("by-department", lambda department: department.name),
        ("by-digital-takeup", lambda department: department.takeup),
        ("by-cost", lambda department: department.cost),
        ("by-data-coverage", lambda department: department.data_coverage),
        ("by-transactions-per-year", lambda department: department.volume),
    ]
    generate_sorted_pages(departments, 'all-services', department_sort_orders)


    csv_map = map_services_to_csv_data(services)
    render_csv(csv_map, 'transaction-volumes.csv')

    # Copy the assets folder entirely, as well
    dir_util.copy_tree('assets', '%s/assets' % OUTPUT_DIR)
