var GOVUK = GOVUK || {};
GOVUK.transactionsExplorer = GOVUK.transactionsExplorer || {};

GOVUK.transactionsExplorer.loadSearchData = function (dataUrl, callback) {
    $.ajax({
        method: "GET",
        url: dataUrl,
        dataType: "json"
    }).done(callback);
};

GOVUK.transactionsExplorer.isSearchMatch = (function () {
    var SEARCH_FIELDS = [
        "agencyOrBodyAbbreviation",
        "service",
        "departmentAbbreviation",
        "agencyOrBody",
        "department",
        "keywords",
        "category"
    ];

    var isSearchMatch = function (searchTerm, service) {
        var search = searchTerm.toLowerCase();
        var found = false;

        $.each(SEARCH_FIELDS, function (i, field) {
            var valueToSearch;

            if (field === "keywords") {
                valueToSearch = service[field].join(' ').toLowerCase();
            } else {
                valueToSearch = service[field].toLowerCase();
            }

            if (valueToSearch.search(search) >= 0) {
                found = true;
                return false; // breaks the loop
            }
        });

        return found;
    };

    return isSearchMatch;
}());

GOVUK.transactionsExplorer.serviceComparator = (function () {
    var propertyComparator = function (property) {
        return function (anObject, anotherObject) {
            if (anObject[property] < anotherObject[property]) return -1;
            if (anObject[property] > anotherObject[property]) return 1;
            if (anObject[property] === anotherObject[property]) return 0;
        };
    };

    var reversed = function (comparator) {
        return function (anObject, anotherObject) {
            return -comparator(anObject, anotherObject);
        };
    };

    var buildPropertyComparator = function (direction, property) {
        if (direction === 'descending') {
            return reversed(propertyComparator(property));
        }
        return propertyComparator(property)
    };

    var serviceComparator = function (property, direction) {
        var compare = buildPropertyComparator(direction, property);

        return function (anObject, anotherObject) {
            if (!anObject[property]) return 1;
            if (!anotherObject[property]) return -1;
            return compare(anObject, anotherObject);
        };
    };

    return serviceComparator;
}());

GOVUK.transactionsExplorer.search = (function () {
    var SORT_PROPERTIES = {
        'service': 'service',
        'category': 'category',
        'agency': 'agencyOrBodyAbbreviation',
        'volume': 'transactionsPerYear'
    };

    var data = [],
        loaded = false,
        cachedQuery = undefined;

    var load = function (dataUrl) {
        loaded = false;
        GOVUK.transactionsExplorer.loadSearchData(dataUrl, function (loadedData) {
            data = loadedData;
            loaded = true;
            if (cachedQuery) {
                GOVUK.transactionsExplorer.search.performSearch(cachedQuery, data);
            }
        });
    };

    var searchServices = function (params, services) {
        var sortProperty = SORT_PROPERTIES[params.sortBy];
        var comparator = GOVUK.transactionsExplorer.serviceComparator(sortProperty, params.direction);

        var matchingSearch = function (service) {
            return GOVUK.transactionsExplorer.isSearchMatch(params.keyword, service);
        };

        return $.grep(services, matchingSearch).sort(comparator);
    };

    var normaliseSortParams = function (queryParams) {
        if (!SORT_PROPERTIES[queryParams.sortBy]) queryParams.sortBy = 'volume';
        queryParams.direction = queryParams.direction === 'ascending' ? 'ascending' : 'descending';
    };

    var performSearch = function (queryParams) {
        normaliseSortParams(queryParams);

        if (loaded) {
            var results = GOVUK.transactionsExplorer.search.searchServices(queryParams, data);
            GOVUK.transactionsExplorer.searchResultsTable.update(results, queryParams);
        } else {
            cachedQuery = queryParams;
        }

        $("table tbody").highlight(queryParams.keyword);
    };

    return {
        load: load,
        searchServices: searchServices,
        performSearch: performSearch
    };
}());

GOVUK.transactionsExplorer.wireSearchForm = function (ids, search, parameters) {
    var searchBox = $(ids.inputId),
        searchForm = $(ids.formId),
        loaded = false;

    if (parameters.keyword) {
        search.load(searchForm.data("search"));
        loaded = true;
        searchBox.val(parameters.keyword);
        search.performSearch(parameters);
    }

    searchBox.on('focus', function (event) {
        if (!loaded) {
            search.load(searchForm.data("search"));
            loaded = true;
        }
    });
};

GOVUK.transactionsExplorer.searchResultsTable = (function () {
    var table = undefined,
        ROW_TEMPLATE = "<tr class='i-get-removed'>" +
            "<th class='js-row-header'></th>" +
            "<td class='js-row-abbr'></td>" +
            "<td class='js-row-category'></td>" +
            "<td class='js-row-transaction'></td>" +
            "<td class='js-row-transactions amount'></td>" +
            "</tr>",
        NO_RESULTS_TEMPLATE = "<tr><th colspan='5'>No results for that query</th></tr>";

    var wireTable = function (id) {
        table = $(id);
    };

    var rowHeader = function (serviceName, link) {
        if (link) {
            return '<a href="' + link + '">' + serviceName + '</a>';
        } else {
            return serviceName;
        }
    };

    var columnHeader = function (text, link, currentDirection) {
        if (currentDirection) {
            return '<a href="' + link + '">' + text + '</a><span class="sort-ind">' + currentDirection + '</span>';
        }
        return '<a href="' + link + '">' + text + '</a>';
    };

    var transactionLink = function (transactionLink) {
        if (transactionLink) {
            return '<a rel="external" href="' + transactionLink + '">Access service</a>';
        } else {
            return "&nbsp;";
        }
    };

    var abbreviation = function (abbreviation, title) {
        if (!abbreviation) {
            return title;
        }
        return '<abbr title="' + title + '">' + abbreviation + '</abbr>'
    }

    var transactionsPerYear = function (transactionsPerYear) {
        if (transactionsPerYear) {
            return transactionsPerYear.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        } else {
            return "&nbsp;";
        }
    };

    var updateColumnHeaders = function (queryParams) {
        $('th.sortable').each(function (i, elem) {
            var th = $(elem);
            var link = function (direction) {
                return 'search?' + $.param({ keyword: queryParams.keyword, sortBy: th.data('sort-by'), direction: direction});
            }

            if (th.data('sort-by') !== queryParams.sortBy) {
                th.html(columnHeader(th.text(), link(th.data('default-direction'))));
            } else if (queryParams.direction === 'ascending') {
                th.html(columnHeader(th.text(), link('descending'), '&#9650;'));
                th.addClass("sorted ascending");
            } else {
                th.html(columnHeader(th.text(), link('ascending'), '&#9660;'));
                th.addClass("sorted descending");
            }
        });
    };

    var update = function (services, queryParams) {
        var rows = [];

        $.each(services, function (i, service) {
            var row = $(ROW_TEMPLATE);
            row.find('.js-row-header').html(rowHeader(service['service'], service['detailsLink']));
            row.find('.js-row-abbr').html(abbreviation(service['agencyOrBodyAbbreviation'], service['agencyOrBody']));
            row.find('.js-row-category').html(service['category']);
            row.find('.js-row-transaction').html(transactionLink(service['transactionLink']));
            row.find('.js-row-transactions').html(transactionsPerYear(service['transactionsPerYear']));

            rows.push('<tr>' + row.html() + '</tr>');
        });

        if (rows.length === 0) {
            table.find('tbody').html(NO_RESULTS_TEMPLATE);
        } else {
            table.find('tbody').html(rows.join(''));
        }

        updateColumnHeaders(queryParams);
    };

    return {
        wireTable: wireTable,
        update: update
    };
}());

GOVUK.transactionsExplorer.getQueryParams = function (search) {
    var decode = function (string) {
        if (!string) return string;
        return decodeURIComponent(string).replace(/\+/g, ' ');
    };

    var searchParts = search.substring(1).split('&');
    var params = {};
    for (var i = 0; i < searchParts.length; ++i) {
        var entry = searchParts[i].split('=', 2);
        params[decode(entry[0])] = decode(entry[1]);
    }
    return params;
};

GOVUK.transactionsExplorer.initSearch = function () {
    $(function () {
        GOVUK.transactionsExplorer.searchResultsTable.wireTable('#transactions-table');
        GOVUK.transactionsExplorer.wireSearchForm({
                formId: '#search',
                inputId: '#search-box',
                buttonId: '#search-button'
            },
            GOVUK.transactionsExplorer.search,
            GOVUK.transactionsExplorer.getQueryParams(document.location.search));
    });
};
