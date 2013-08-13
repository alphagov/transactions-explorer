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
        "keywords"
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

    var load = function () {
        GOVUK.transactionsExplorer.loadSearchData("search.json", function (loadedData) {
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

    var performSearch = function (query) {
        if (loaded) {
            var results = GOVUK.transactionsExplorer.search.searchServices(query, data);
            GOVUK.transactionsExplorer.searchResultsTable.update(results);
        } else {
            cachedQuery = query;
        }
    };

    return {
        load: load,
        searchServices: searchServices,
        performSearch: performSearch
    };
}());

GOVUK.transactionsExplorer.wireSearchForm = function(ids, search) {
    var searchBox = $(ids.inputId),
        searchButton = $(ids.buttonId),
        loaded = false;

    searchBox.on('focus', function (event) {
        if (!loaded) {
            search.load();
            loaded = true;
        }
    });

    $('#search').on('submit', function (event) {
        search.performSearch(searchBox.val());
        event.preventDefault();
    });
};

GOVUK.transactionsExplorer.searchResultsTable = (function () {
    var table = undefined,
        ROW_TEMPLATE =  "<tr class='i-get-removed'>" + 
                            "<th class='js-row-header'></th>" + 
                            "<td class='js-row-abbr'></td>" +
                            "<td class='js-row-category'></td>" + 
                            "<td class='js-row-transaction'></td>" + 
                            "<td class='js-row-transactions'></td>" +
                        "</tr>";
    
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
            return '<a href="' + transactionLink + '">Access service</a>'; 
        } else {
            return "&nbsp;";
        }
    };

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
            row.find('.js-row-abbr').html(service['agencyOrBodyAbbreviation']);
            row.find('.js-row-category').html(service['category']);
            row.find('.js-row-transaction').html(transactionLink(service['transactionLink']));
            row.find('.js-row-transactions').html(transactionsPerYear(service['transactionsPerYear']));
        
            rows.push('<tr>' + row.html() + '</tr>');
        });
        table.find('tbody').html(rows.join(''));
    };

    return {
        wireTable: wireTable,
        update: update
    };
}());
