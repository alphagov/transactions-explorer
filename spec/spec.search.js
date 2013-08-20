describe("Searching for services on the transaction explorer. ", function() {

    describe('getQueryParams', function () {
        it('should return query params as an object', function () {
            var params = GOVUK.transactionsExplorer.getQueryParams('?a=1&b=2');
            expect(params).toEqual({a:'1', b:'2'});
        });

        it('should decode escape sequences', function() {
            var params = GOVUK.transactionsExplorer.getQueryParams('?keyword=son%20of%20keyword');
            expect(params).toEqual({keyword:'son of keyword'});
        });

        it('should replaces +\'s with spaces', function() {
            var params = GOVUK.transactionsExplorer.getQueryParams('?keyword=lost+in+keyword');
            expect(params).toEqual({keyword:'lost in keyword'});
        });

        it('should handle params with no value', function() {
            var params = GOVUK.transactionsExplorer.getQueryParams('?param1&param2');
            expect(params).toEqual({param1: undefined, param2: undefined});
        });

        it('should return empty params if there is no querystring', function() {
            var params = GOVUK.transactionsExplorer.getQueryParams('');
            expect(params).toEqual({});
        });

    });

    describe("The search form", function() {
        var fakeSearch = undefined,
            ENTER_KEY = 13;

        beforeEach(function() {
            $('<form id="search"></form>').appendTo('body');
            $('<input id="search-box" type="text"></input>').appendTo('#search');
            $('<button id="search-button" type="submit">Find</button>').appendTo('#search');
            fakeSearch = {
                load: jasmine.createSpy('load search data'),
                performSearch: jasmine.createSpy('perform a search')
            };
            GOVUK.transactionsExplorer.wireSearchForm({
                searchForm: "#search",
                inputId: "#search-box",
                buttonId: "#search-button"
            }, fakeSearch, {});
        });

        afterEach(function() {
            $('#search').remove();
        });

        describe("Searching based on query parameters", function () {
            it('should search for the keyword if provided in the wireup', function () {
                GOVUK.transactionsExplorer.wireSearchForm({
                    searchForm: "#search",
                    inputId: "#search-box",
                    buttonId: "#search-button"
                }, fakeSearch, {keyword: 'iAmAKeyWord'});
                expect(fakeSearch.performSearch).toHaveBeenCalledWith({keyword: 'iAmAKeyWord'});
            });
        });

        it("should load search data the first time the search box gets focus", function() {
            $('#search-box').trigger($.Event('focus'));
            expect(fakeSearch.load).toHaveBeenCalled();
        });

        it("should not try to load the search data multiple times", function() {
            $('#search-box').trigger($.Event('focus'));
            $('#search-box').trigger($.Event('focus'));
            expect(fakeSearch.load.calls.length).toBe(1);
        });

    });

    describe("Search matching", function() {
        describe("score:", function() {
            it('should return true if the service contains the search term', function() {
                var service = buildService({department: "Department of Wibble"});

                var result = GOVUK.transactionsExplorer.isSearchMatch('wibble', service);

                expect(result).toBe(true);
            });

            it('should return false if the service does not match the search term', function() {
                var result = GOVUK.transactionsExplorer.isSearchMatch('mongoose', buildService({}));

                expect(result).toBe(false);
            });

            it('should ignore case when matching', function() {
                var service = buildService({department: "Department of Ninjas"});

                var result = GOVUK.transactionsExplorer.isSearchMatch('NINJAS', service);

                expect(result).toBe(true);
            });

            it('should search for keywords', function () {
                var service = buildService({keywords: ['pirates','parrots','grog']});

                var result = GOVUK.transactionsExplorer.isSearchMatch('grog', service);

                expect(result).toBe(true);
            });
        });
    });

    describe("performSearch", function () {
        beforeEach(function () {
            spyOn(GOVUK.transactionsExplorer.search, 'searchServices');
            spyOn(GOVUK.transactionsExplorer.searchResultsTable, 'update');
            spyOn(GOVUK.transactionsExplorer, 'loadSearchData').andCallFake(function (_, callback) {
                callback(null);
            });

            GOVUK.transactionsExplorer.search.load();
        });

        it("should invoke searchServices with query parameters", function() {
            GOVUK.transactionsExplorer.search.performSearch(
                {keyword: 'coffee', sortBy: 'service', direction: 'ascending'}
            );

            expect(GOVUK.transactionsExplorer.search.searchServices).toHaveBeenCalledWith(
                {keyword: 'coffee', sortBy: 'service', direction: 'ascending'}, null);
        });

        it("should apply default values of sortBy and direction if missing", function() {
            GOVUK.transactionsExplorer.search.performSearch(
                {keyword: 'tea'}
            );

            expect(GOVUK.transactionsExplorer.search.searchServices).toHaveBeenCalledWith(
                {keyword: 'tea', sortBy: 'volume', direction: 'descending'}, null);
        });

        it("should fallback to default values if actual values are bonkers", function() {
            GOVUK.transactionsExplorer.search.performSearch(
                {keyword: 'tea', sortBy: 'bonkers-property', direction: 'left'}
            );

            expect(GOVUK.transactionsExplorer.search.searchServices).toHaveBeenCalledWith(
                {keyword: 'tea', sortBy: 'volume', direction: 'descending'}, null);
        });

    });

    describe("Loading on slow connections", function () {

        var completeLoading;

        beforeEach(function () {
            spyOn(GOVUK.transactionsExplorer.search, 'searchServices');
            spyOn(GOVUK.transactionsExplorer, 'loadSearchData').andCallFake(function (_, callback) {
                completeLoading = callback;
            });
            spyOn(GOVUK.transactionsExplorer.searchResultsTable, 'update');
        });

        it("should cache most recent query until the search json is loaded", function () {
            GOVUK.transactionsExplorer.search.load();

            GOVUK.transactionsExplorer.search.performSearch({keyword: 'coffee'});
            GOVUK.transactionsExplorer.search.performSearch({keyword: 'tea'});
            GOVUK.transactionsExplorer.search.performSearch({keyword: 'bacon'});
            
            expect(GOVUK.transactionsExplorer.search.searchServices).not.toHaveBeenCalled();

            completeLoading("received data");

            expect(GOVUK.transactionsExplorer.search.searchServices).toHaveBeenCalledWith(
                {keyword: 'bacon', sortBy: jasmine.any(String), direction: jasmine.any(String)}, "received data");
        });
    });

    describe("Search", function() {
        it("should perform a search", function () {
            var services = [{
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
            }];
            searchResults = GOVUK.transactionsExplorer.search.searchServices({keyword: 'second'}, services);
            expect(searchResults.length).toEqual(1);
            expect(searchResults[0].department).toBe('second department');
        });

        it("should sort results according to params", function () {
            var services = [
                buildService({ service: "bbbb", agencyOrBodyAbbreviation: "gds" }),
                buildService({ service: "cccc", agencyOrBodyAbbreviation: "gds" }),
                buildService({ service: "aaaa", agencyOrBodyAbbreviation: "gds" })
            ];

            searchResults = GOVUK.transactionsExplorer.search.searchServices({keyword: 'gds', sortBy: 'service', direction: 'ascending'}, services);

            expect(searchResults[0].service).toBe('aaaa');
            expect(searchResults[1].service).toBe('bbbb');
            expect(searchResults[2].service).toBe('cccc');
        });

        it("should leave empty values at the end regardless of the direction", function () {
            var services = [
                buildService({ agencyOrBodyAbbreviation: "gds", category: "zzzz" }),
                buildService({ agencyOrBodyAbbreviation: "gds", category: "aaaa" }),
                buildService({ agencyOrBodyAbbreviation: "gds", category: "" })
            ];

            searchResults = GOVUK.transactionsExplorer.search.searchServices({keyword: 'gds', sortBy: 'category', direction: 'ascending'}, services);

            expect(searchResults[2].category).toBe('');

            searchResults = GOVUK.transactionsExplorer.search.searchServices({keyword: 'gds', sortBy: 'category', direction: 'descending'}, services);

            expect(searchResults[2].category).toBe('');
        });
    });

    var fakeAjax = undefined;

    beforeEach(function() {
        fakeAjax = spyOn($, 'ajax').andReturn({
            done: function(callback) {
                //no-op
            }
        });
    });

    describe("loading search data", function() {
        it('should ajax in some data when loaded', function() {
            GOVUK.transactionsExplorer.loadSearchData();
            expect(fakeAjax).toHaveBeenCalled();
        });
    });

    describe("Results table", function() {
        beforeEach(function() {
            $('<table id="results"><tbody></tbody></table>').appendTo('body');
        });

        afterEach(function() {
            $('#results').remove();
        });

        it('should update the table with results', function() {
            var resultsTable = $('#results');
            GOVUK.transactionsExplorer.searchResultsTable.wireTable('#results');

            GOVUK.transactionsExplorer.searchResultsTable.update([{
                agencyOrBodyAbbreviation: "AA",
                service: "some service",
                departmentAbbreviation: "DA",
                agencyOrBody: "",
                transactionsPerYear: 9999,
                department: "some department",
                category: "some category",
                transactionLink: "http://www.bar.com",
                keywords: [],
                detailsLink: "http://www.foo.com"
            }]);

            expect(resultsTable.find('th').first().html()).toBe('<a href="http://www.foo.com">some service</a>');
            expect(resultsTable.find('tr td').first().text()).toBe('AA');
            expect($(resultsTable.find('tr td').get(1)).text()).toBe('some category');
            expect($(resultsTable.find('tr td').get(2)).html()).toBe('<a rel="external" href="http://www.bar.com">Access service</a>');
            expect($(resultsTable.find('tr td').get(3)).text()).toBe('9,999');
        });

        it('should not display links when they don\'t exist', function() {
            var resultsTable = $('#results');
            GOVUK.transactionsExplorer.searchResultsTable.wireTable('#results');

            GOVUK.transactionsExplorer.searchResultsTable.update([{
                agencyOrBodyAbbreviation: "AA",
                service: "some service",
                departmentAbbreviation: "DA",
                agencyOrBody: "",
                transactionsPerYear: 9999,
                department: "some department",
                category: "some category",
                transactionLink: null,
                keywords: [],
                detailsLink: null 
            }]);

            expect(resultsTable.find('th').first().html()).toBe('some service');
            expect(resultsTable.find('tr td').first().html()).toBe('<abbr title="">AA</abbr>');
            expect($(resultsTable.find('tr td').get(1)).text()).toBe('some category');
            expect($(resultsTable.find('tr td').get(2)).html()).toBe('&nbsp;');
            expect($(resultsTable.find('tr td').get(3)).text()).toBe('9,999'); 
        });

        it('should format big numbers with commas', function () {
            GOVUK.transactionsExplorer.searchResultsTable.wireTable('#results');
            GOVUK.transactionsExplorer.searchResultsTable.update([{
                agencyOrBodyAbbreviation: "AA",
                service: "some service",
                departmentAbbreviation: "DA",
                agencyOrBody: "",
                transactionsPerYear: 2345987,
                department: "some department",
                category: "some category",
                transactionLink: null,
                keywords: [],
                detailsLink: null 
            }]);

            var resultsTable = $('#results');
            expect($(resultsTable.find('tr td').get(3)).text()).toBe('2,345,987'); 
        });

        it('should display null numbers as blank', function () {
            GOVUK.transactionsExplorer.searchResultsTable.wireTable('#results');
            GOVUK.transactionsExplorer.searchResultsTable.update([{
                agencyOrBodyAbbreviation: "AA",
                service: "some service",
                departmentAbbreviation: "DA",
                agencyOrBody: "",
                transactionsPerYear: null,
                department: "some department",
                category: "some category",
                transactionLink: null,
                keywords: [],
                detailsLink: null 
            }]);

            var resultsTable = $('#results');
            expect($(resultsTable.find('tr td').get(3)).html()).toBe('&nbsp;'); 
        });

        it('should remove old results when updated with new ones', function() {
            var table = $('table');
            table.find('tbody').append('<tr id="mr-row"><th>foo</th><td>bar</td></tr>');
            GOVUK.transactionsExplorer.searchResultsTable.wireTable('#results');
            GOVUK.transactionsExplorer.searchResultsTable.update({
                agencyOrBodyAbbreviation: "AA",
                service: "some service",
                departmentAbbreviation: "DA",
                agencyOrBody: "",
                transactionsPerYear: 9999,
                department: "some department",
                category: "some category",
                transactionLink: "temp link",
                keywords: []
            });

            expect($('#mr-row').length).toBe(0);
        });
    });
});

function buildService(properties) {
    var defaultProperties = {
                agencyOrBodyAbbreviation: "DEF",
                service: "default service name",
                departmentAbbreviation: "DEFDEP",
                agencyOrBody: "default agency",
                transactionsPerYear: 0,
                department: "default department",
                category: "default category",
                transactionLink: "default link",
                keywords: []
            };
    return $.extend(defaultProperties, properties);
}
