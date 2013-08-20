var GOVUK = GOVUK || {};
GOVUK.transactionsExplorer = GOVUK.transactionsExplorer || {};

GOVUK.transactionsExplorer.loadSearchData = function(dataUrl, callback) {
    $.ajax({
        method: "GET",
        url: dataUrl,
        dataType: "json"
    }).done(callback);
};

GOVUK.transactionsExplorer.scoreService = (function () {
    var SEARCH_FIELDS = [
        "agencyOrBodyAbbreviation",
        "service",
        "departmentAbbreviation",
        "agencyOrBody",
        "department",
        "keywords",
        "category"
    ];

    var scoreService = function (searchTerm, service) {
        var score = 0;
        $.each(SEARCH_FIELDS, function (i, field) {
            var valueToSearch,
                termToUse = searchTerm.toLowerCase();
            if (field === "keywords") {
                valueToSearch = service[field].join(' ').toLowerCase();
            } else {
                valueToSearch = service[field].toLowerCase();
            }

            if (valueToSearch.search(termToUse) >= 0) {
                //FIXME this is pretty inefficient but $ doesn't provide a reduce
                score = service.transactionsPerYear || 1;
            }

        });
        return score;
    };

    return scoreService;
}());

GOVUK.transactionsExplorer.search = (function () {
    var data = [],
        loaded = false,
        cachedQuery = undefined;

    var load = function (dataUrl) {
        GOVUK.transactionsExplorer.loadSearchData(dataUrl, function (loadedData) {
            data = loadedData;
            loaded = true;
            if (cachedQuery) {
                GOVUK.transactionsExplorer.search.performSearch(cachedQuery, data);
            }
        });
    };

    var searchServices = function (query, services) {
        var scoredServices = $.map(services, function (service, index) {
            return {
                service: service,
                score: GOVUK.transactionsExplorer.scoreService(query, service)
            };
        });
        var matchedServices = $.grep(scoredServices, function(n, i) {
            return (n.score > 0);
        }).sort(function (first, next) {
            if (first.score > next.score) return -1;
            if (first.score < next.score) return 1;
            if (first.score === next.score) return 0;
        });
        return $.map(matchedServices, function(scoredService, index) {
            return scoredService.service;
        });
    };

    var performSearch = function (queryParams) {
        if (loaded) {
            var results = GOVUK.transactionsExplorer.search.searchServices(queryParams.keyword, data);
            GOVUK.transactionsExplorer.searchResultsTable.update(results);
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

GOVUK.transactionsExplorer.wireSearchForm = function(ids, search, parameters) {
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
        ROW_TEMPLATE =  "<tr class='i-get-removed'>" + 
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
            return '<a href="' + link  + '">' + serviceName + '</a>';
        } else {
            return serviceName;
        }
    };
    
    var transactionLink = function (transactionLink) {
        if (transactionLink) {
            return '<a rel="external" href="' + transactionLink + '">Access service</a>'; 
        } else {
            return "&nbsp;";
        }
    };

    var abbreviation = function (abbreviation, title) {
        if (!abbreviation) { return title; }
        return '<abbr title="' + title + '">' + abbreviation + '</abbr>'
    }

    var transactionsPerYear = function (transactionsPerYear) {
        if (transactionsPerYear) {
            return transactionsPerYear.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        } else {
            return "&nbsp;";
        }
    };

    var update = function (services) {
        var rows = [];

        $.each(services, function (i, service) {
            var row = $(ROW_TEMPLATE);
            row.find('.js-row-header').html(rowHeader(service['service'], service['detailsLink']));
            row.find('.js-row-abbr').html(abbreviation(service['agencyOrBodyAbbreviation'],service['agencyOrBody']));
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

    };

    return {
        wireTable: wireTable,
        update: update
    };
}());

GOVUK.transactionsExplorer.getQueryParams = function(search) {
    var decode = function(string) {
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
}

GOVUK.transactionsExplorer.initSearch = function () {
    $(function () {
    GOVUK.transactionsExplorer.wireSearchForm({
        formId: '#search',
        inputId: '#search-box',
        buttonId: '#search-button'
        },
        GOVUK.transactionsExplorer.search,
        GOVUK.transactionsExplorer.getQueryParams(document.location.search));
    GOVUK.transactionsExplorer.searchResultsTable.wireTable('#transactions-table');
    });
};

