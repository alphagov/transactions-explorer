Transactions Explorer
=====================

[![Build Status](https://travis-ci.org/alphagov/transactions-explorer.png?branch=master)](https://travis-ci.org/alphagov/transactions-explorer)

Generates a static HTML version of the [Transactions Explorer][tx].

[tx]: http://transactionsexplorer.cabinetoffice.gov.uk

## Prerequisites

This README expects you to have the `virtualenv` and `virtualenvwrapper` python packages installed. You can do this with the following command.

```
pip install virtualenv virtualenvwrapper
```

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
* Fetch the data through either of the methods below:
  * Run `python fetch_csv.py`. This will authenticate against Google in your browser, then download the Transactions Explorer document to `data/services.csv`. It can be parametrized with the following arguments:
      * `--client-secrets`: Google API client secrets JSON file (default: `data/client_secrets.json`)
      * `--oauth-tokens`: Google API OAuth tokens file (default: `data/tokens.dat`)
  * Run `./fetch_data.sh` script. It will perform the above task, installing the required dependencies and using the default values.

[console]: https://code.google.com/apis/console/


### Generating site

* Generate the site with `python create_pages.py`. It can be parametrized with
the following argument:
  * `--services-data`: Services CSV datafile (default: `data/services.csv`)
  * `--path-prefix`: Prefix for generated URL paths (default: `/`)
  * `--static-digests` Path to manifest file containing assets digests (default: None) You can download the current digests from https://assets.digital.cabinet-office.gov.uk/static/manifest.yml
* [alternative] Generate the site with `./build_artefact.sh` script. It will run the above command with all the defaults.
* [optional] symlink the contents of assets/javascripts to output/assets/javascripts 
for faster feedback than running create_pages each time.
* run `./serve.sh` 
* visit `http://localhost:8080/all-services`.
* dance.


## Testing

Unit tests can be run with `./run_tests.sh`.

After generating the site as described above you can test
it generated correctly by running `nosetests` (or `nosetests -a feature`
to skip unit tests.

## Building and Deployment

Build pipe line:

`transactions-explorer -> transactions-explorer-build-artefacts -> transactions-explorer-deploy*`

The `transactions-explorer` task runs the tests and triggers `transactions-explorer-build-artefacts`
if the tests all pass.

The `transactions-explorer-build-artefacts` task runs `build.sh`. This kicks off a number of steps
which generate the site as a deployable tar ball for each environment (preview, staging and production)

The `build.sh` steps:

- Fetch data
    - Pull down the latest version of the csv data, the locations of the credentials files are set as environment variables in `build.sh`
- Generate the treemap fallbacks for browsers where d3.js doesn't work (`build_treemaps.sh`)
    - Generates the site locally and hosts it on the python test server
    - Runs phantomjs (managed by a subprocess in python because it tends to misbehave see: `create_treemap_fallbacks.py`)
    - The phantomjs subprocess visits each page with a treemap (listed in `create_treemap_fallbacks.py`) and extracts the treemap HTML to files in `output/treemaps`
- Generate the deployable version of the site for each environment (`build_artefact.sh`)
    - Runs `build_artefact.sh` with the environment specific variables
    - Copies in the treemap fallbacks created above
    - Packages the site (this is the contents of the `output` directory) as a tar ball and puts it in the `artefacts` folder

Once finished the build job will trigger a deployment to preview, other deployments must be triggered manually.
