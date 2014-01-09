#!/bin/bash -e

if [ -z "$VIRTUAL_ENV" ]; then
    echo "ERROR: You are not running within a virtual environment" >&2
    exit 1
fi

if [ -n "${CLIENT_SECRETS}" ]; then FETCH_ARGS="${FETCH_ARGS} --client-secrets ${CLIENT_SECRETS}"; fi
if [ -n "${OAUTH_TOKENS}" ];   then FETCH_ARGS="${FETCH_ARGS} --oauth-tokens ${OAUTH_TOKENS}"; fi

python fetch_csv.py $FETCH_ARGS
