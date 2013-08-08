import unittest

from hamcrest import *
from nose.tools import nottest

from test.features import BrowserTest


class test_create_pages(BrowserTest):

    def test_about_page(self):
         pass
        self.browser.visit("http://0.0.0.0:8000/high-volume-services/by-transactions-per-year/descending")
        assert_that(self.browser.find_by_css('h1').text, is_('High-volume services'))

    @nottest
    def test_all_services(self):
        self.browser.visit("http://0.0.0.0:8000/all-services")
        assert_that(self.browser.find_by_css('h1').text, is_("All Services"))
        assert_that(self.browser.find_by_css('#navigation .current').text, is_("All services"))

