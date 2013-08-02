Service Explorer
================
Generates a static HTML version of the [Transactions Explorer][tx].

[tx]: http://transactionsexplorer.cabinetoffice.gov.uk


Using
-----
Set up a python virtualenv, activate it, and then install required modules
with `pip install -r requirements.txt`.

Create a new installed application in the [Google APIs console][console], 
download the `client_secrets.json` file and store it in `data/`, then
run `python fetch_csv.py`. This will authenticate against Google in your
browser, then download the Service Explorer detail to `data/services.csv`.

Generate the site with `python create_pages.py`.

[console]: https://code.google.com/apis/console/
