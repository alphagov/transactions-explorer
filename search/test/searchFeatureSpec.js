describe("end to end search", function () {
    beforeEach(function () {
        $('<input id="searchInput" type="text"></input>').appendTo('body');
        $('<button id="searchButton" type=submit>Find</button>').appendTo('body');
        $('<table id="results"><tbody></tbody></table>').appendTo('body');
        spyOn($,'ajax').andReturn({ done: function (callback) {
            callback([{
                agencyOrBodyAbbreviation: "FA",
                service: "some service for agency 1",
                departmentAbbreviation: "FD",
                agencyOrBody: "",
                transactionsPerYear: 7,
                department: "first department",
                category: "some category",
                transactionLink: "temp link",
                keywords: []
            },{
                agencyOrBodyAbbreviation: "SA",
                service: "some service for agency 2",
                departmentAbbreviation: "SD",
                agencyOrBody: "",
                transactionsPerYear: 9999,
                department: "second department",
                category: "some category",
                transactionLink: "temp link",
                keywords: []
            }]);
        }});
    });

    afterEach(function () {
        $('#searchInput').remove();
        $('#searchButton').remove();
        $('#results').remove();
    });

    it('should search for services', function () {
        GOVUK.transactionsExplorer.searchResultsTable.wireTable('#results');
        GOVUK.transactionsExplorer.wireSearchForm(
            {
                inputId: '#searchInput',
                buttonId: '#searchButton'
            },
            GOVUK.transactionsExplorer.search
        );

        $('#searchInput').trigger('focus');
        $('#searchInput').val('FA');
        $('#searchButton').click();

        expect($('#results tr').length).not.toBe(0);
    });
});
