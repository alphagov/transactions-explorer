#!/bin/bash -e

mkdir -p artefacts
rm -f artefacts/*

VIRTUALENV_DIR=/var/tmp/virtualenvs/$(echo ${JOB_NAME} | tr ' ' '-')
export PIP_DOWNLOAD_CACHE=/var/tmp/pip_download_cache

virtualenv --clear --no-site-packages $VIRTUALENV_DIR
source $VIRTUALENV_DIR/bin/activate

pip install -r requirements.txt

if [ -n "${CLIENT_SECRETS}" ]; then FETCH_ARGS="${FETCH_ARGS} --client-secrets ${CLIENT_SECRETS}"; fi
if [ -n "${OAUTH_TOKENS}" ];   then FETCH_ARGS="${FETCH_ARGS} --oauth-tokens ${OAUTH_TOKENS}"; fi

python fetch_csv.py $FETCH_ARGS
python create_pages.py

cd output
tar -zcvf ../artefacts/service-explorer.tgz .
