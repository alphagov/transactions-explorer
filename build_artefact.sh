#!/bin/bash -e

if [ -z "$VIRTUAL_ENV" ]; then
  echo "ERROR: You are not running within a virtual environment" >&2
  exit 1
fi

mkdir -p artefacts; rm -f artefacts/*
mkdir -p output; rm -Rf output/*

if [ -n "${CLIENT_SECRETS}" ]; then FETCH_ARGS="${FETCH_ARGS} --client-secrets ${CLIENT_SECRETS}"; fi
if [ -n "${OAUTH_TOKENS}" ];   then FETCH_ARGS="${FETCH_ARGS} --oauth-tokens ${OAUTH_TOKENS}"; fi

python fetch_csv.py $FETCH_ARGS

if [ -n "${PATH_PREFIX}" ]; then CREATE_ARGS="${CREATE_ARGS} --path-prefix ${PATH_PREFIX}"; fi
if [ -n "${ASSET_PREFIX}" ]; then CREATE_ARGS="${CREATE_ARGS} --asset-prefix ${ASSET_PREFIX}"; fi

python create_pages.py $CREATE_ARGS

cd output
tar -zcvf ../artefacts/transactions-explorer.tgz .
