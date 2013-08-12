from hamcrest import *
from nose.tools import nottest

from test.features import BrowserTest
from test.features.support import table_from


class GenerateDepartmentPages(BrowserTest):

    def test_generates_title(self):
        self.browser.visit("http://0.0.0.0:8000/department/def")
        title = self.browser.find_by_css('#whitehall-wrapper').text

        assert_that(title, is_(u'Department of Electronic Freedom'))

    def test_generate_data_coverage(self):
        self.browser.visit("http://0.0.0.0:8000/department/abc")
        coverage = self.browser.find_by_css('#data-coverage-notice').text

        assert_that(coverage, is_(u'Department data coverage: 66.7%\n(taken from 1 high volume services)'))

    def test_do_not_generate_data_coverage_if_no_high_volume_services(self):
        self.browser.visit("http://0.0.0.0:8000/department/low")

        assert_that(self.browser.is_element_not_present_by_css('#data-coverage-notice'),
                    is_(True))

    def test_generate_transactions_table(self):
        self.browser.visit("http://0.0.0.0:8000/department/abc")
        table = table_from(self.browser.find_by_css('tbody tr'))

        assert_that(table, is_([
            [u'Service 1', u'ABC', u'Exciting service', u'Access service', u'4,820,000'],
            [u'Service 2', u'ABC', u'', u'', u'17,150'],
            [u'Service 3', u'ABC', u'Lame service', u'', u'2,141'],
        ]))

