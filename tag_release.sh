#!/usr/bin/env bash

set -e

if [ $TRAVIS = "true" -a $TRAVIS_BRANCH = "master" ]; then
    git remote add origin-release git://github.com/alphagov/service-explorer.git
    git fetch origin-release
    git checkout -b release origin-release/release
    git merge master
    git tag "release-${TRAVIS_BUILD_NUMBER}"
    git push "https://${GITHUB_ACCESS_TOKEN}:x-oauth-basic@github.com/alphagov/service-explorer.git" release
    git push --tags "https://${GITHUB_ACCESS_TOKEN}:x-oauth-basic@github.com/alphagov/service-explorer.git"
fi
