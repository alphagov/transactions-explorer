#!/bin/bash -e

. ./create_virtualenv.sh "$(echo ${JOB_NAME} | tr ' ' '-')"
./run_tests.sh
