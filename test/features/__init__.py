from unittest import TestCase
from splinter import Browser
from test.features.support.stub_server import HttpStub


def setup_package():
    HttpStub.start()


def teardown_package():
    HttpStub.stop()


class BrowserTest(TestCase):
    def setUp(self):
        self.browser = Browser('phantomjs', wait_time=3)

    def tearDown(self):
        self.browser.quit()
