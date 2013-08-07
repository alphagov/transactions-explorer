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
        with Browser('phantomjs', wait_time=3) as browser:
            browser.visit("http://0.0.0.0:8000/high-volume-services/by-transactions-per-year/descending.html")
            assert_that(browser.is_text_present('High-volume services'),
                        is_(True))
