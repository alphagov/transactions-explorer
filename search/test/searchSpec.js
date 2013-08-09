describe("Searching for services on the transaction explorer. ", function () {
    describe("The search form", function () {
        
        var fakeSearch = undefined,
            ENTER_KEY = 13;

        beforeEach(function () {
            $('<input id="search-box" type="text"></input>').appendTo('body');
            $('<button id="search-button" type="submit">Find</button>').appendTo('body');
            fakeSearch = {
                load: jasmine.createSpy('load search data'),
                performSearch: jasmine.createSpy('perform a search')
            };
            GOVUK.transactionsExplorer.wireSearchForm(
                { inputId: "#search-box", buttonId: "#search-button" },
                fakeSearch
            );
        });

        afterEach(function () {
            $('#search-box').remove();
            $('#search-button').remove();
        });

        it("should load search data the first time the search box gets focus", function () {
            $('#search-box').trigger($.Event('focus'));
            expect(fakeSearch.load).toHaveBeenCalled();
        });

        it("should not try to load the search data multiple times", function () {
            $('#search-box').trigger($.Event('focus'));
            $('#search-box').trigger($.Event('focus'));
            expect(fakeSearch.load.calls.length).toBe(1);
        });

        it("should perform a search when enter is pressed", function () {
            $('#search-box').val('woozle wozzle');
            $('#search-box').trigger($.Event('keydown', { keyCode: ENTER_KEY }));
            expect(fakeSearch.performSearch).toHaveBeenCalledWith('woozle wozzle');
        });

        it("should perform a search when the search button is clicked", function () {
            $('#search-box').val('woozle wozzle weazle');
            $('#search-button').click();
            expect(fakeSearch.performSearch).toHaveBeenCalledWith('woozle wozzle weazle');
        });
    });

    describe("Search", function () {
    
    });
});

