Service Explorer
================

[![Build Status](https://travis-ci.org/alphagov/service-explorer.png?branch=master)](https://travis-ci.org/alphagov/service-explorer)

Generates a static HTML version of the [Transactions Explorer][tx].

[tx]: http://transactionsexplorer.cabinetoffice.gov.uk


Using
-----
Set up a python virtualenv, activate it, and then install required modules
with `pip install -r requirements.txt`.

### Fetching data

* Create a new installed application in the [Google APIs console][console],
with "Drive API" service enabled, download the `client_secrets.json` file
and store it in `data/`
* Run `python fetch_csv.py`. This will athenticate against Google in your browser, 
then download the Service Explorer detail to `data/services.csv`. It can be 
parametrized with the following arguments:
  * `--client-secrets`: Google API client secrets JSON file (default: `data/client_secrets.json`)
  * `--oauth-tokens`: Google API OAuth tokens file (default: `data/tokens.dat`)

[console]: https://code.google.com/apis/console/

### Generating site


* Generate the site with `python create_pages.py`. It can be parametrized with
the following argument:
  * `--services-data`: Services CSV datafile (default: `data/services.csv`)
* [optional] symlink the contents of assets/javascripts to output/assets/javascripts 
for faster feedback than running create_pages each time.
* run python `test/features/support/stub_server.py &`. 
* visit localhost:8000/all-services or similar.
* dance.


Testing
-------
Unit tests can be run with `nosetests -a '!feature'`

After generating the site as described above you can test
it generated correctly by running `nosetests` (or `nosetests -a feature`
to skip unit tests.
