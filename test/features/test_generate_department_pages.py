from hamcrest import *
from nose.tools import nottest

from test.features import BrowserTest
from test.features.support import table_from


class GenerateDepartmentPages(BrowserTest):

    def test_generates_title(self):
        self.browser.visit("http://0.0.0.0:8000/department/def/by-transactions-per-year/descending")
        title = self.browser.find_by_css('#whitehall-wrapper').text

        assert_that(title, is_(u'Department of Electronic Freedom'))

    def test_generate_data_coverage(self):
        self.browser.visit("http://0.0.0.0:8000/department/abc/by-transactions-per-year/descending")
        coverage = self.browser.find_by_css('#data-coverage-notice').text

        assert_that(coverage, is_(u'Department data coverage: 66.7%\n(taken from 1 high volume services)'))

    @nottest
    def test_do_not_generate_data_coverage_if_no_high_volume_services(self):
        """
        Disabled because it randomly throws an WebDriver exception that fails
        the test, even if the markup is correct
        """
        self.browser.visit("http://0.0.0.0:8000/department/low/by-transactions-per-year/descending")

        assert_that(self.browser.is_element_not_present_by_css('#data-coverage-notice', wait_time=3),
                    is_(True))

    def test_generate_transactions_table(self):
        self.browser.visit("http://0.0.0.0:8000/department/abc/by-transactions-per-year/descending")
        table = table_from(self.browser.find_by_css('tbody tr'))

        assert_that(table, is_([
            [u'Service 1', u'GDS', u'Exciting service', u'Access service', u'4,820,000'],
            [u'Service 2', u'GDS', u'', u'', u'17,150'],
            [u'Service 3', u'Another Government', u'Lame service', u'', u'2,141'],
        ]))

    def test_treemap_has_one_leaf_node_for_each_transaction(self):
        self.browser.visit("http://0.0.0.0:8000/department/def/by-transactions-per-year/descending")
        treemap_nodes = self.browser.find_by_css('.treemap .leaf')

        assert_that(len(treemap_nodes), is_(5))

    def test_first_element_sorted_by_transaction_name_descending(self):
        self.browser.visit("http://0.0.0.0:8000/department/abc/by-name/descending")
        assert_that(self.browser.find_by_css('tbody tr th').text, is_(u"Service 3"))

    def test_first_element_sorted_by_transaction_name_descending(self):
        self.browser.visit("http://0.0.0.0:8000/department/abc/by-name/ascending")
        assert_that(self.browser.find_by_css('tbody tr th').text, is_(u"Service 1"))

    def test_first_element_sorted_by_agency_descending(self):
        self.browser.visit("http://0.0.0.0:8000/department/abc/by-agency/descending")
        assert_that(self.browser.find_by_css('tbody tr th').text, is_(u"Service 1"))

    def test_first_element_sorted_by_agency_ascending(self):
        self.browser.visit("http://0.0.0.0:8000/department/abc/by-agency/ascending")
        assert_that(self.browser.find_by_css('tbody tr th').text, is_(u"Service 3"))

    def test_first_element_sorted_by_category_descending(self):
        self.browser.visit("http://0.0.0.0:8000/department/abc/by-category/descending")
        assert_that(self.browser.find_by_css('tbody tr th').text, is_(u"Service 3"))

    def test_first_element_sorted_by_category_ascending(self):
        self.browser.visit("http://0.0.0.0:8000/department/abc/by-category/ascending")
        assert_that(self.browser.find_by_css('tbody tr th').text, is_(u"Service 2"))

    def test_first_element_sorted_by_transaction_per_year_descending(self):
        self.browser.visit("http://0.0.0.0:8000/department/abc/by-transactions-per-year/descending")
        assert_that(self.browser.find_by_css('tbody tr th').text, is_(u"Service 1"))

    def test_first_element_sorted_by_transaction_per_year_ascending(self):
        self.browser.visit("http://0.0.0.0:8000/department/abc/by-transactions-per-year/ascending")
        assert_that(self.browser.find_by_css('tbody tr th').text, is_(u"Service 3"))
