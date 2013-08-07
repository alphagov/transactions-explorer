import unittest

from hamcrest import *
from splinter import Browser

from support.stub_server import HttpStub


class test_create_pages(unittest.TestCase):

    def setUp(self):
        HttpStub.start()

    def tearDown(self):
        HttpStub.stop()

    def test_about_page(self):
        with Browser() as browser:
            browser.visit("http://0.0.0.0:8000/high-volume-services/by-transactions-per-year/descending.html")
            assert_that(browser.find_by_css('h1').text, is_('High-volume services'))

    def test_all_services(self):
        with Browser() as browser:
            browser.visit("http://0.0.0.0:8000/all-services.html")
            assert_that(browser.find_by_css('h1').text, is_("All Services"))
            assert_that(browser.find_by_css('#navigation .current').text, is_("All services"))

