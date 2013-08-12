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
        loaded = false;

    var load = function () {
        GOVUK.transactionsExplorer.loadSearchData("search.json", function (loadedData) {
            data = loadedData;
            loaded = true;
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
        ENTER_KEY = 13,
        loaded = false;

    searchBox.on('focus', function (event) {
        if (!loaded) {
            search.load();
            loaded = true;
        }
    });

    searchBox.on('keydown', function (event) {
        if (event.keyCode === ENTER_KEY) {
            search.performSearch(searchBox.val());
        }
    });

    searchButton.on('click', function (event) {
        search.performSearch(searchBox.val());
    });
};

GOVUK.transactionsExplorer.searchResultsTable = (function () {
    var table = undefined;

    var wireTable = function (id) {
        table = $(id);
    };

    var update = function (services) {
        var rows = [],
            ROW_CONTENTS = ['service', 'agencyOrBodyAbbreviation', 'category', 'transactionLink', 'transactionsPerYear'],
            detailsLink = function (serviceName, link) {
                if (link) {
                    return '<th><a href="' + link  + '">' + serviceName + '</a></th>';
                } else {
                    return '<th>' + serviceName + '</th>';
                }
            },
            transactionLink = function (transactionLink) {
                if (transactionLink) {
                    return '<td><a href="' + transactionLink + '">Access service</a></td>'; 
                } else {
                    return "<td>&nbsp;</td>";
                }
            };

        $.each(services, function (i, service) {
            var row = '';
            $.each(ROW_CONTENTS, function (i, rowKey) {
                if (i === 0) {
                    row += detailsLink(service[rowKey], service.detailsLink);
                } else if (rowKey === 'transactionLink') {
                    row += transactionLink(service[rowKey]);
                } else {
                    row += '<td>' + service[rowKey] + '</td>';
                }
            });
            rows.push('<tr>' + row + '</tr>');
        });
        table.find('tbody').html(rows.join(''));
    };

    return {
        wireTable: wireTable,
        update: update
    };
}());

