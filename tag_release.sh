#!/usr/bin/env bash

set -e

if [ $TRAVIS = "true" -a $TRAVIS_BRANCH = "master" ]; then
    git checkout release
    git merge master
    git tag "release-${TRAVIS_BUILD_NUMBER}"
    git push "https://${GITHUB_ACCESS_TOKEN}:x-oauth-basic@github.com/alphagov/service-explorer.git"
fi
