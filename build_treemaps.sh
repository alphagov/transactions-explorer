#!/bin/bash -e

if [ -z "$VIRTUAL_ENV" ]; then
    echo "ERROR: You are not running within a virtual environment" >&2
    exit 1
fi

mkdir -p artefacts
mkdir -p output; rm -Rf output/*

python create_pages.py

python ./test/features/support/test_server.py 46576 >> /dev/null 2>&1 &

server_pid=$!
echo pid of server is $server_pid

python create_treemap_fallbacks.py 'http://localhost:46576/'

kill $server_pid

cd output/treemaps
tar -zcvf "../../artefacts/${TREEMAP_ARTEFACT_NAME}" .

cd ../../
rm -Rf output
