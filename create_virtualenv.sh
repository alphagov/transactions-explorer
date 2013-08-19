#!/bin/bash -e

VENV_NAME=$1

VIRTUALENV_DIR="/var/tmp/virtualenvs/$VENV_NAME"
export PIP_DOWNLOAD_CACHE=/var/tmp/pip_download_cache

virtualenv --clear --no-site-packages $VIRTUALENV_DIR
source $VIRTUALENV_DIR/bin/activate

pip install -r requirements.txt
