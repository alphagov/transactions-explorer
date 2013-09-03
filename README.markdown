Transactions Explorer
=====================

[![Build Status](https://travis-ci.org/alphagov/transactions-explorer.png?branch=master)](https://travis-ci.org/alphagov/transactions-explorer)

Generates a static HTML version of the [Transactions Explorer][tx].

[tx]: http://transactionsexplorer.cabinetoffice.gov.uk


## Using the app

You need to use a machine that has a web browser installed in order to
authenticate with Google. If you're using a GDS machine, this means you should
not perform any of these steps in the GDS development VM.

Set up a Python virtualenv, activate it, and then install required packages
with `pip install -r requirements.txt`.

    $ cd ~/govuk
    $ git clone git@github.com:alphagov/transactions-explorer.git
    $ cd transactions-explorer
    $ mkvirtualenv transactions-explorer
    $ pip install -r requirements.txt

After setting this up for the first time, you just need to run
`workon transactions-explorer` in future.


### Fetching data

* Create a new installed application in the [Google APIs console][console],
with "Drive API" service enabled, download the `client_secrets.json` file
and store it in `data/`
* Run `python fetch_csv.py`. This will authenticate against Google in your browser,
then download the Transactions Explorer document to `data/services.csv`. It can be
parametrized with the following arguments:
  * `--client-secrets`: Google API client secrets JSON file (default: `data/client_secrets.json`)
  * `--oauth-tokens`: Google API OAuth tokens file (default: `data/tokens.dat`)

[console]: https://code.google.com/apis/console/


### Generating site

* Generate the site with `python create_pages.py`. It can be parametrized with
the following argument:
  * `--services-data`: Services CSV datafile (default: `data/services.csv`)
  * `--path-prefix`: Prefix for generated URL paths (default: `/`)
  * `--static-digests` Path to manifest file containing assets digests (default: None) You can download the current digests from https://assets.digital.cabinet-office.gov.uk/static/manifest.yml
* [optional] symlink the contents of assets/javascripts to output/assets/javascripts 
for faster feedback than running create_pages each time.
* run python `test/features/support/stub_server.py &`. 
* visit localhost:8000/all-services or similar.
* dance.


## Testing

Unit tests can be run with `./run_tests.sh`.

After generating the site as described above you can test
it generated correctly by running `nosetests` (or `nosetests -a feature`
to skip unit tests.

