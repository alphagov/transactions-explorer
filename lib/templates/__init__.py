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

jinja.globals['CSV_LOCATION'] = '/transaction-volumes.csv'
jinja.globals['GA_ACCOUNT'] = 'UA-36369871-1'
jinja.globals['GA_DOMAIN'] = 'gov.uk'

jinja.filters['as_magnitude'] = number_as_magnitude
jinja.filters['as_financial_magnitude'] = number_as_financial_magnitude
jinja.filters['as_percentage'] = number_as_percentage
jinja.filters['as_percentage_change'] = number_as_percentage_change
jinja.filters['as_grouped_number'] = number_as_grouped_number
jinja.filters['as_absolute_url'] = string_as_absolute_url
jinja.filters['as_asset_url'] = string_as_asset_url
jinja.filters['as_static_url'] = string_as_static_url
jinja.filters['slugify'] = slugify


def render(template_name, out, vars):
    template = jinja.get_template(template_name)
    page = template.render(**vars)
    with _output_file(out) as output:
        output.write(page.encode('utf8'))


def render_csv(maps, out):
    with _output_file(out) as output:
        writer = csv.writer(output, dialect="excel")
        writer.writerows(maps)


def render_search_json(maps, out):
    with _output_file(out) as output:
        json.dump(maps, output)


def _output_file(path):
    print path
    output_path = os.path.join(output_dir, path)
    create_directory(os.path.dirname(output_path))
    return open(output_path, 'w')
