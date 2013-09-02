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

cd output
cp "../artefacts/${TREEMAP_ARTEFACT_NAME}" .
mkdir treemaps && tar -C "treemaps" -xvf ${TREEMAP_ARTEFACT_NAME}
tar -zcvf "../artefacts/${ARTEFACT_NAME}" .
