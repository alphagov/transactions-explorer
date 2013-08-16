#!/bin/bash

set -eo pipefail

. ./create_virtualenv.sh $VIRTUALENV_NAME
./build_artefact.sh
