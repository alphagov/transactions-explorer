from hamcrest import *

from test.features import BrowserTest


class GenerateAllServicesPages(BrowserTest):


    def test_sort_by_department_descending(self):
        self.browser.visit("http://0.0.0.0:8000/all-services/by-department/descending")
        assert_that(self.browser.find_by_css('tbody tr th a').text, is_(u"Lower Order Workgroups"))

    def test_sort_by_department_ascending(self):
        self.browser.visit("http://0.0.0.0:8000/all-services/by-department/ascending")
        assert_that(self.browser.find_by_css('tbody tr th a').text, is_(u"Agency for Beautiful Code"))

    def test_sort_by_digit_take_up_descending(self):
        self.browser.visit("http://0.0.0.0:8000/all-services/by-takeup/descending")
        assert_that(self.browser.find_by_css('tbody tr th a').text, is_(u"Agency for Beautiful Code"))

    def test_sort_by_digit_take_up_ascending(self):
        self.browser.visit("http://0.0.0.0:8000/all-services/by-takeup/ascending")
        assert_that(self.browser.find_by_css('tbody tr th a').text, is_(u"Department of Electronic Freedom"))

    def test_sort_by_total_cost_descending(self):
        self.browser.visit("http://0.0.0.0:8000/all-services/by-cost/descending")
        assert_that(self.browser.find_by_css('tbody tr th a').text, is_(u"Department of Electronic Freedom"))

    def test_sort_by_total_cost_ascending(self):
        self.browser.visit("http://0.0.0.0:8000/all-services/by-cost/ascending")
        assert_that(self.browser.find_by_css('tbody tr th a').text, is_(u"Agency for Beautiful Code"))

    def test_sort_by_data_coverage_descending(self):
        self.browser.visit("http://0.0.0.0:8000/all-services/by-data-coverage/descending")
        assert_that(self.browser.find_by_css('tbody tr th a').text, is_(u"Agency for Beautiful Code"))

    def test_sort_by_data_coverage_ascending(self):
        self.browser.visit("http://0.0.0.0:8000/all-services/by-data-coverage/ascending")
        assert_that(self.browser.find_by_css('tbody tr th a').text, is_(u"Department of Electronic Freedom"))

    def test_sort_by_volume_descending(self):
        self.browser.visit("http://0.0.0.0:8000/all-services/by-volume/descending")
        assert_that(self.browser.find_by_css('tbody tr th a').text, is_(u"Department of Electronic Freedom"))

    def test_sort_by_volume_ascending(self):
        self.browser.visit("http://0.0.0.0:8000/all-services/by-volume/ascending")
        assert_that(self.browser.find_by_css('tbody tr th a').text, is_(u"Lower Order Workgroups"))

