from hamcrest import *
from nose.tools import nottest

from test.features import BrowserTest


class test_create_pages(BrowserTest):

    def test_about_page(self):
        self.browser.visit("http://0.0.0.0:8000/high-volume-services/by-transactions-per-year/descending")
        assert_that(self.browser.find_by_css('h1').text, is_('High-volume services'))

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
        assert_that(self.browser.find_by_css('#navigation .current').text, is_("All services"))

