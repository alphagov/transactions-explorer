import unittest

from hamcrest import *
from nose.tools import nottest

from test.features import BrowserTest


class test_create_pages(BrowserTest):

    def test_about_page(self):
        self.browser.visit("http://0.0.0.0:8000/high-volume-services/"
                           "by-transactions-per-year/descending")
        assert_that(self.browser.find_by_css('h1').text,
                    is_('High-volume services'))

    def test_home_page(self):
        self.browser.visit("http://0.0.0.0:8000/home")

        headlines = self.browser.find_by_css('.headline')

        departments = headlines[0].text
        services = headlines[1].text
        transactions = headlines[2].text

        assert_that(departments, contains_string('16'))
        assert_that(services, contains_string('654'))
        assert_that(transactions, contains_string('1.31bn'))

    @nottest
    def test_all_services(self):
        self.browser.visit("http://0.0.0.0:8000/all-services")
        assert_that(self.browser.find_by_css('h1').text, is_("All Services"))
        assert_that(self.browser.find_by_css('#navigation .current').text,
                    is_("All services"))

    def test_sort_by_department_descending(self):
        self.browser.visit("http://0.0.0.0:8000/all-services/by-department/descending")
        assert_that(self.browser.find_by_css('tbody tr th a').text, is_(u"Ministry of Justice"))

    def test_sort_by_department_ascending(self):
        self.browser.visit("http://0.0.0.0:8000/all-services/by-department/ascending")
        assert_that(self.browser.find_by_css('tbody tr th a').text, is_(u"Attorney General's Office"))

    def test_sort_by_digit_take_up_descending(self):
        self.browser.visit("http://0.0.0.0:8000/all-services/by-digital-takeup/descending")
        assert_that(self.browser.find_by_css('tbody tr th a').text, is_(u"Cabinet Office"))

    def test_sort_by_digit_take_up_ascending(self):
        self.browser.visit("http://0.0.0.0:8000/all-services/by-digital-takeup/ascending")
        assert_that(self.browser.find_by_css('tbody tr th a').text, is_(u"Ministry of Justice"))

    def test_sort_by_total_cost_descending(self):
        self.browser.visit("http://0.0.0.0:8000/all-services/by-cost/descending")
        assert_that(self.browser.find_by_css('tbody tr th a').text, is_(u"Department for Work and Pensions"))

    def test_sort_by_total_cost_ascending(self):
        self.browser.visit("http://0.0.0.0:8000/all-services/by-cost/ascending")
        assert_that(self.browser.find_by_css('tbody tr th a').text, is_(u"Cabinet Office"))

    def test_sort_by_data_coverage_descending(self):
        self.browser.visit("http://0.0.0.0:8000/all-services/by-data-coverage/descending")
        assert_that(self.browser.find_by_css('tbody tr th a').text, is_(u"Department for Work and Pensions"))

    def test_sort_by_data_coverage_ascending(self):
        self.browser.visit("http://0.0.0.0:8000/all-services/by-data-coverage/ascending")
        assert_that(self.browser.find_by_css('tbody tr th a').text, is_(u"Ministry of Justice"))

    def test_sort_by_volume_descending(self):
        self.browser.visit("http://0.0.0.0:8000/all-services/by-transactions-per-year/descending")
        assert_that(self.browser.find_by_css('tbody tr th a').text, is_(u"HM Revenue and Customs"))

    def test_sort_by_volume_ascending(self):
        self.browser.visit("http://0.0.0.0:8000/all-services/by-transactions-per-year/ascending")
        assert_that(self.browser.find_by_css('tbody tr th a').text, is_(u"Department for International Development"))
