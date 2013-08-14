import csv
import simplejson as json
import os
from jinja2 import Environment, FileSystemLoader
from lib.filesystem import create_directory
from lib.filters import *
from lib.slugify import slugify


output_dir = None

jinja = Environment(
    loader=FileSystemLoader(searchpath='templates', encoding='utf-8'),
    trim_blocks=True,
    lstrip_blocks=True,
    extensions=['jinja2.ext.with_']
)

jinja.globals['STATIC_HOST'] = 'https://assets.digital.cabinet-office.gov.uk/static'
jinja.globals['CSV_LOCATION'] = '/transaction-volumes.csv'
jinja.globals['GA_ACCOUNT'] = 'UA-36369871-1'
jinja.globals['GA_DOMAIN'] = 'gov.uk'

jinja.filters['as_magnitude'] = number_as_magnitude
jinja.filters['as_financial_magnitude'] = number_as_financial_magnitude
jinja.filters['as_percentage'] = number_as_percentage
jinja.filters['as_percentage_change'] = number_as_percentage_change
jinja.filters['as_grouped_number'] = number_as_grouped_number
jinja.filters['as_absolute_path'] = string_as_absolute_path
jinja.filters['slugify'] = slugify


def render(template_name, out, vars):
    print out

    template = jinja.get_template(template_name)
    page = template.render(**vars)
    output_path = os.path.join(output_dir, out)
    create_directory(os.path.dirname(output_path))
    with open(output_path, 'w') as output:
        output.write(page.encode('utf8'))


def render_csv(maps, out):
    with open(os.path.join(output_dir, out), 'w') as output:
        writer = csv.writer(output, dialect="excel")
        writer.writerows(maps)


def render_search_json(maps, out):
    with open(os.path.join(output_dir, out), 'w') as output:
        json.dump(maps, output)
