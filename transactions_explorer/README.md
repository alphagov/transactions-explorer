# Overview #
Script to grab the URLs that we shouldn't break as part of the migration

```
scrapy crawl transactions-explorer 2>&1 | grep DEBUG | grep GET | grep -v Filtered | awk '/./ { print substr($8, 0, length($8)) " " substr($6, 2, 3) }' | sort | uniq > urls.txt
```

