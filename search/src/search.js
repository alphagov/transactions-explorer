var GOVUK = GOVUK || {};
GOVUK.transactionsExplorer = GOVUK.transactionsExplorer || {};

GOVUK.transactionsExplorer.loadSearchData = function(dataUrl, callback) {
    $.ajax({
        method: "GET",
        url: dataUrl,
        dataType: "json"
    }).done(callback);
};

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

