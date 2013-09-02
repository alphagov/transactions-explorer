#!/bin/bash -e

if [ -z "$VIRTUAL_ENV" ]; then
    echo "ERROR: You are not running within a virtual environment" >&2
    exit 1
fi

mkdir -p artefacts
mkdir -p output; rm -Rf output/*

if [ -n "${PATH_PREFIX}" ]; then CREATE_ARGS="${CREATE_ARGS} --path-prefix ${PATH_PREFIX}"; fi
if [ -n "${ASSET_PREFIX}" ]; then CREATE_ARGS="${CREATE_ARGS} --asset-prefix ${ASSET_PREFIX}"; fi
CREATE_ARGS="${CREATE_ARGS} --static-digests data/static-digests.yml"

python create_pages.py $CREATE_ARGS

#python ./test/features/support/test_server.py 46576 >> /dev/null 2>&1 &

server_pid=$!
echo pid is $server_pid

python create_treemap_fallbacks.py 'http://localhost:46576/'

kill $server_pid

cd output
tar -zcvf "../artefacts/${ARTEFACT_NAME}" .
