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
        "department"
    ];

    var scoreService = function (searchTerm, service) {
        var score = 0;
        $.each(SEARCH_FIELDS, function (i, field) {
            var valueToSearch = service[field].toLowerCase(),
                termToUse = searchTerm.toLowerCase();

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
    var data, loaded;

    var load = function () {
        GOVUK.transactionsExplorer.loadSearchData("search.json", function (loadedData) {
            data = loadedData;
            loaded = true;
        });
    };

    var performSearch = function (query) {
        if (loaded) {
            console.log($.grep(data, function (service) {
                return service['Department'].search(query) >= 0;
            }));
        }
    };

    return {
        load: load,
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
            ROW_CONTENTS = ['service', 'agencyOrBodyAbbreviation', 'category', 'transactionLink', 'transactionsPerYear'];

        $.each(services, function (i, service) {
            var row = '';
            $.each(ROW_CONTENTS, function (i, rowKey) {
                if (i === 0) { 
                    row += '<th>' + service[rowKey] + '</th>';
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

