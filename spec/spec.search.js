describe("Searching for services on the transaction explorer. ", function() {
    describe('extracting keywords from document.location.search', function () {
        it('should trim out the keyword (search query)', function () {
            var keyword = GOVUK.transactionsExplorer.getSearchKeyword('?keyword=iAmKeyword');
            expect(keyword).toBe('iAmKeyword');
        });
        
        it('should deal with spaces (search query)', function () {
            var keyword = GOVUK.transactionsExplorer.getSearchKeyword('?keyword=son%20of%20keyword');
            expect(keyword).toBe('son of keyword');
        });

        it('should ignore extra keywords', function () {
            var keyword1 = GOVUK.transactionsExplorer.getSearchKeyword('?keyword=revengeOfKeyword&foo=bar');
            var keyword2 = GOVUK.transactionsExplorer.getSearchKeyword('?bar=foo&keyword=returnOfKeyword');
            var keyword3 = GOVUK.transactionsExplorer.getSearchKeyword('?zap=monkey&keyword=the%20mask%20of%20keyword&foo=bar');
            
            expect(keyword1).toBe('revengeOfKeyword');
            expect(keyword2).toBe('returnOfKeyword');
            expect(keyword3).toBe('the mask of keyword');
        });

        it('should replaces +\'s with spaces', function () {
            var keyword = GOVUK.transactionsExplorer.getSearchKeyword('?keyword=lost+in+keyword');

            expect(keyword).toBe('lost in keyword');
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
            }, fakeSearch);
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
                }, fakeSearch, 'iAmAKeyWord');
                expect(fakeSearch.performSearch).toHaveBeenCalledWith('iAmAKeyWord');
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

    describe("Result ranking", function() {
        describe("score:", function() {
            it('should score a search result with the number of transactions if the service contains the search term', function() {
                var score = GOVUK.transactionsExplorer.scoreService('wibble', {
                    agencyOrBodyAbbreviation: "DOW",
                    service: "Request to wibble",
                    departmentAbbreviation: "DOW",
                    agencyOrBody: "",
                    transactionsPerYear: 4500,
                    department: "Department of Wibble",
                    category: "",
                    keywords: []
                });

                expect(score).toBe(4500);
            });

            it('should return a score of 0 if the service does not match the search term', function() {
                var score = GOVUK.transactionsExplorer.scoreService('mongoose', {
                    agencyOrBodyAbbreviation: "DOW",
                    service: "Request to wibble",
                    departmentAbbreviation: "DOW",
                    agencyOrBody: "",
                    transactionsPerYear: 4500,
                    department: "Department of Wibble",
                    category: "",
                    keywords: []
                });

                expect(score).toBe(0);
            });

            it('should return a score of 1 if the service matches the search term but does not have any transactions', function() {
                var score = GOVUK.transactionsExplorer.scoreService('Ninjas', {
                    agencyOrBodyAbbreviation: "DON",
                    service: "Dial a ninja",
                    departmentAbbreviation: "DON",
                    agencyOrBody: "",
                    transactionsPerYear: null,
                    department: "Department of Ninjas",
                    category: "",
                    keywords: []
                });

                expect(score).toBe(1);
            });

            it('should ignore case when ranking results', function() {
                var score = GOVUK.transactionsExplorer.scoreService('NINJAS', {
                    agencyOrBodyAbbreviation: "DON",
                    service: "Dial a ninja",
                    departmentAbbreviation: "DON",
                    agencyOrBody: "",
                    transactionsPerYear: 7777,
                    department: "Department of Ninjas",
                    category: "",
                    keywords: []
                });

                expect(score).toBe(7777);
            });

            it('should search for keywords', function () {
                var score = GOVUK.transactionsExplorer.scoreService('grog', {
                    agencyOrBodyAbbreviation: "DOP",
                    service: "Post a pirate",
                    departmentAbbreviation: "DOP",
                    agencyOrBody: "",
                    transactionsPerYear: 5000,
                    department: "Department of Pirates",
                    category: "",
                    keywords: ['pirates','parrots','grog']
                });

                expect(score).toBe(5000);
            });
        });
    });

    describe("Loading on slow connections", function () {
        beforeEach(function () {
            spyOn(GOVUK.transactionsExplorer.search, 'searchServices');
            spyOn(GOVUK.transactionsExplorer, 'loadSearchData').andCallFake(function (_, callback) {
                callback(null);
            });
            spyOn(GOVUK.transactionsExplorer.searchResultsTable, 'update');
        });

        it("should cache most recent query until the search json is loaded", function () {
            GOVUK.transactionsExplorer.search.performSearch('coffee');
            GOVUK.transactionsExplorer.search.performSearch('tea');
            GOVUK.transactionsExplorer.search.performSearch('bacon');
            
            expect(GOVUK.transactionsExplorer.search.searchServices).not.toHaveBeenCalled();
            
            GOVUK.transactionsExplorer.search.load();
            
            expect(GOVUK.transactionsExplorer.search.searchServices).toHaveBeenCalledWith('bacon', null);
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
            searchResults = GOVUK.transactionsExplorer.search.searchServices('second', services);
            expect(searchResults.length).toEqual(1);
            expect(searchResults[0].department).toBe('second department');
        });

        it("should order results according to score", function () {
            var services = [{
                agencyOrBodyAbbreviation: "gds",
                service: "lower rated",
                departmentAbbreviation: "co",
                agencyOrBody: "",
                transactionsPerYear: 23,
                department: "first department",
                category: "some category",
                transactionLink: "temp link",
                keywords: []
            },{
                agencyOrBodyAbbreviation: "gds",
                service: "highly rated",
                departmentAbbreviation: "co",
                agencyOrBody: "",
                transactionsPerYear: 999,
                department: "second department",
                category: "some category",
                transactionLink: "temp link",
                keywords: []
            },{
                agencyOrBodyAbbreviation: "nomatch",
                service: "highly rated",
                departmentAbbreviation: "foo",
                agencyOrBody: "",
                transactionsPerYear: 999,
                department: "second department",
                category: "some category",
                transactionLink: "temp link",
                keywords: []
            }];
            searchResults = GOVUK.transactionsExplorer.search.searchServices('gds', services);
            expect(searchResults.length).toEqual(2);
            expect(searchResults[0].service).toBe('highly rated');
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

