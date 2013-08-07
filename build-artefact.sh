#!/bin/bash

VIRTUALENV_DIR=/var/tmp/virtualenvs/$(echo ${JOB_NAME} | tr ' ' '-')
export PIP_DOWNLOAD_CACHE=/var/tmp/pip_download_cache

virtualenv --clear --no-site-packages $VIRTUALENV_DIR
source $VIRTUALENV_DIR/bin/activate

pip install -r requirements.txt

python fetch_csv.py
python create_pages.py

mkdir -p artefacts
cd output
zip -r ../artefacts/service-explorer.zip .
