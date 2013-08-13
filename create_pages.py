#!/usr/bin/env python
import sys
from distutils import dir_util

import unicodecsv
from lib.params import parse_args_for_create

from lib.service import Service, latest_quarter, sorted_ignoring_empty_values, Department

from lib import templates
from lib.csv import map_services_to_csv_data, map_services_to_dicts

from lib.service import Service, latest_quarter, sorted_ignoring_empty_values,\
    total_transaction_volume
from lib.slugify import slugify
from lib.templates import render, render_csv, render_search_json


OUTPUT_DIR = 'output'

templates.output_dir = OUTPUT_DIR

arguments = parse_args_for_create(sys.argv[1:])
input = arguments.services_data

data = open(input)

reader = unicodecsv.DictReader(data)

services = [Service(details=row) for row in reader]
high_volume_services = [service for service in services if service.high_volume]
latest_quarter = latest_quarter(high_volume_services)

departments = set(s.department for s in services)


def generate_sorted_pages(items, page_name, output_prefix, sort_orders, extra_variables={}):
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
                   out="%s/%s/%s.html" % (output_prefix, sort_order, direction),
                   vars=variables)


if __name__ == "__main__":
    render("about-the-data.html", "about-data.html", {})
    render("index.html", "index.html", {
        'departments_count': len(departments),
        'services_count': len(services),
        'total_transactions': total_transaction_volume(services)
    })
    for service in high_volume_services:
        render('service_detail.html',
               out=service.link,
               vars={'service': service,
                     'department': Department(service.department, [service])})

    sort_orders = [
        ("by-name", lambda service: service.name_of_service),
        ("by-department", lambda service: service.abbr),
        ("by-total-cost", lambda service: service.most_recent_kpis['cost']),
        ("by-cost-per-transaction", lambda service: service.most_recent_kpis['cost_per_number']),
        ("by-digital-takeup", lambda service: service.most_recent_kpis['takeup']),
        ("by-transactions-per-year", lambda service: service.most_recent_kpis['volume_num']),
    ]
    generate_sorted_pages(high_volume_services, 'high-volume-services', 'high-volume-services',
                          sort_orders, {'latest_quarter': latest_quarter})

    departments = Department.from_services(services)
    department_sort_orders = [
        ("by-department", lambda department: department.name),
        ("by-digital-takeup", lambda department: department.takeup),
        ("by-cost", lambda department: department.cost),
        ("by-data-coverage", lambda department: department.data_coverage),
        ("by-transactions-per-year", lambda department: department.volume),
    ]
    generate_sorted_pages(departments, 'all-services', 'all-services', department_sort_orders)

    services_sort_orders = [
        ("by-name", lambda service: service.name_of_service),
        ("by-agency", lambda service: service.agency_abbreviation),
        ("by-category", lambda service: service.category),
        ("by-transactions-per-year", lambda service: service.most_up_to_date_volume),
    ]
    for department in departments:
        generate_sorted_pages(department.services, 'department',
                              'department/%s' % slugify(department.abbr),
                              services_sort_orders, {'department': department})

    csv_map = map_services_to_csv_data(services)
    render_csv(csv_map, 'transaction-volumes.csv')

    json_map = map_services_to_dicts(services)
    render_search_json(json_map, 'search.json')

    # Copy the assets folder entirely, as well
    dir_util.copy_tree('assets', '%s/assets' % OUTPUT_DIR)
