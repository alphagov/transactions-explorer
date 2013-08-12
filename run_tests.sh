#!/bin/bash

set -o pipefail

echo "== INSTALLING DEPENDENCIES =="
pip install -q -r requirements.txt --use-mirrors

echo -e "\n== CREATING PAGES FROM FIXTURE =="
python create_pages.py --services-data test/features/fixtures/services-test.csv

echo -e "\n== RUNNING TESTS =="
nosetests -v
