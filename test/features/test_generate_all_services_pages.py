from hamcrest import *

from test.features import BrowserTest
from test.features.support import table_from


class GenerateAllServicesPages(BrowserTest):

    def test_all_services_table(self):
        self.browser.visit("http://0.0.0.0:8000/all-services/by-transactions-per-year/descending")
        table = table_from(self.browser.find_by_css('tbody tr'))

        assert_that(table, is_([
            [u'Department of Electronic Freedom', u'84.7%', u'\xa3157m', u'28%', u'21,117,614'],
            [u'Agency for Beautiful Code', u'100%', u'\xa3482k', u'40%', u'4,839,291'],
            [u'Lower Order Workgroups', u'', u'', u'', u'29,127']
        ]))

    def test_first_element_sort_by_department_descending(self):
        self.browser.visit("http://0.0.0.0:8000/all-services/by-department/descending")
        assert_that(self.browser.find_by_css('tbody tr th a').text, is_(u"Lower Order Workgroups"))

    def test_first_element_sort_by_department_ascending(self):
        self.browser.visit("http://0.0.0.0:8000/all-services/by-department/ascending")
        assert_that(self.browser.find_by_css('tbody tr th a').text, is_(u"Agency for Beautiful Code"))

    def test_first_element_sort_by_digit_take_up_descending(self):
        self.browser.visit("http://0.0.0.0:8000/all-services/by-digital-takeup/descending")
        assert_that(self.browser.find_by_css('tbody tr th a').text, is_(u"Agency for Beautiful Code"))

    def test_first_element_sort_by_digit_take_up_ascending(self):
        self.browser.visit("http://0.0.0.0:8000/all-services/by-digital-takeup/ascending")
        assert_that(self.browser.find_by_css('tbody tr th a').text, is_(u"Department of Electronic Freedom"))

    def test_first_element_sort_by_total_cost_descending(self):
        self.browser.visit("http://0.0.0.0:8000/all-services/by-cost/descending")
        assert_that(self.browser.find_by_css('tbody tr th a').text, is_(u"Department of Electronic Freedom"))

    def test_first_element_sort_by_total_cost_ascending(self):
        self.browser.visit("http://0.0.0.0:8000/all-services/by-cost/ascending")
        assert_that(self.browser.find_by_css('tbody tr th a').text, is_(u"Agency for Beautiful Code"))

    def test_first_element_sort_by_data_coverage_descending(self):
        self.browser.visit("http://0.0.0.0:8000/all-services/by-data-coverage/descending")
        assert_that(self.browser.find_by_css('tbody tr th a').text, is_(u"Agency for Beautiful Code"))

    def test_first_element_sort_by_data_coverage_ascending(self):
        self.browser.visit("http://0.0.0.0:8000/all-services/by-data-coverage/ascending")
        assert_that(self.browser.find_by_css('tbody tr th a').text, is_(u"Department of Electronic Freedom"))

    def test_first_element_sort_by_volume_descending(self):
        self.browser.visit("http://0.0.0.0:8000/all-services/by-transactions-per-year/descending")
        assert_that(self.browser.find_by_css('tbody tr th a').text, is_(u"Department of Electronic Freedom"))

    def test_first_element_sort_by_volume_ascending(self):
        self.browser.visit("http://0.0.0.0:8000/all-services/by-transactions-per-year/ascending")
        assert_that(self.browser.find_by_css('tbody tr th a').text, is_(u"Lower Order Workgroups"))
