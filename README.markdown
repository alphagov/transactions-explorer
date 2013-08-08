Service Explorer
================

[![Build Status](https://travis-ci.org/alphagov/service-explorer.png?branch=master)](https://travis-ci.org/alphagov/service-explorer)

Generates a static HTML version of the [Transactions Explorer][tx].

[tx]: http://transactionsexplorer.cabinetoffice.gov.uk


Using
-----
Set up a python virtualenv, activate it, and then install required modules
with `pip install -r requirements.txt`.

Create a new installed application in the [Google APIs console][console],
with "Drive API" service enabled, download the `client_secrets.json` file
and store it in `data/`, then run `python fetch_csv.py`. This will 
authenticate against Google in your browser, then download the Service 
Explorer detail to `data/services.csv`.

Generate the site with `python create_pages.py`.

[console]: https://code.google.com/apis/console/


Testing
-------
Unit tests can be run with `nosetests -a '!feature'`

After generating the site as described above you can test
it generated correctly by running `nosetests` (or `nosetests -a feature`
to skip unit tests.
