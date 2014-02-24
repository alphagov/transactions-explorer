#!/bin/bash

set -o pipefail

if [ -z "$VIRTUAL_ENV" ]; then
  echo "ERROR: You are not running within a virtual environment" >&2
  exit 1
fi

echo "== INSTALLING DEPENDENCIES =="
pip install -q -r requirements.txt

echo -e "\n== CREATING PAGES FROM FIXTURE =="
python create_pages.py --services-data test/features/fixtures/services-test.csv

echo -e "\n== RUNNING TESTS =="
nosetests -v
