#!/usr/bin/env python

import unicodecsv
import re

from lib.service import Service

SERVICES_DATA = 'data/services.csv'

data = open(SERVICES_DATA)
reader = unicodecsv.DictReader(data)
for row in reader:
    service = Service(details=row)
    print service.name
