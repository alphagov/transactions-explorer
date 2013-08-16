#!/bin/bash -e

if [ -n "$USE_VIRTUALENV" ]; then
    VIRTUALENV_DIR="/var/tmp/virtualenvs/$USE_VIRTUALENV"
    export PIP_DOWNLOAD_CACHE=/var/tmp/pip_download_cache

    virtualenv --clear --no-site-packages $VIRTUALENV_DIR
    source $VIRTUALENV_DIR/bin/activate

    pip install -q -r requirements.txt --use-mirrors
elif [ -z "$VIRTUAL_ENV" ]; then
    echo "ERROR: You are not running within a virtual environment" >&2
    exit 1
fi

mkdir -p artefacts; rm -f artefacts/*
mkdir -p output; rm -Rf output/*

curl https://assets.digital.cabinet-office.gov.uk/static/manifest.yml > data/static-digests.yml

if [ -n "${CLIENT_SECRETS}" ]; then FETCH_ARGS="${FETCH_ARGS} --client-secrets ${CLIENT_SECRETS}"; fi
if [ -n "${OAUTH_TOKENS}" ];   then FETCH_ARGS="${FETCH_ARGS} --oauth-tokens ${OAUTH_TOKENS}"; fi

python fetch_csv.py $FETCH_ARGS

if [ -n "${PATH_PREFIX}" ]; then CREATE_ARGS="${CREATE_ARGS} --path-prefix ${PATH_PREFIX}"; fi
if [ -n "${ASSET_PREFIX}" ]; then CREATE_ARGS="${CREATE_ARGS} --asset-prefix ${ASSET_PREFIX}"; fi
CREATE_ARGS="${CREATE_ARGS} --static-digests data/static-digests.yml"

python create_pages.py $CREATE_ARGS

cd output
tar -zcvf ../artefacts/transactions-explorer.tgz .
