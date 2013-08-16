# Overview #
Script to grab the URLs that we shouldn't break as part of the migration

```
scrapy crawl transactions-explorer 2>&1 | grep DEBUG | grep GET | grep -v Filtered | awk '/./ { print substr($8, 0, length($8)) " " substr($6, 2, 3) }' | sort | uniq > urls.txt
```

## Updating the redirections

Once the found URLs have been entered into a CSV file compatible with
the [redirector][redirector], `perl update_redirections.pl` will update
the CSV with the new destinations (this only needs to be done once).

Testing the redirections is done with `prove -l test_redirections.t`.

[redirector]:https://github.com/alphagov/redirector
