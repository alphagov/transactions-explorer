#!/bin/bash -e

echo "Building from version ${APPLICATION_VERSION}"

export CLIENT_SECRETS="/etc/google/oauth/client_secrets.json"
export OAUTH_TOKENS="/var/lib/google/oauth/drive.db"
export PATH_PREFIX="/performance/transactions-explorer/"
export TREEMAP_ARTEFACT_NAME="treemaps.tgz"

. ./create_virtualenv.sh "transactions-explorer-build"
./fetch_data.sh

./build_treemaps.sh

ASSET_HOST="https://assets-origin.preview.alphagov.co.uk" ARTEFACT_NAME="transactions-explorer-preview.tgz" ./build_artefact.sh
ASSET_HOST="https://assets-origin.production.alphagov.co.uk" ARTEFACT_NAME="transactions-explorer-staging.tgz" ./build_artefact.sh
ASSET_HOST="https://assets.digital.cabinet-office.gov.uk" ARTEFACT_NAME="transactions-explorer-production.tgz" ./build_artefact.sh
