from nose.plugins.attrib import attr
from unittest import TestCase
from splinter import Browser
from test.features.support.test_server import TestServer


def setup_package():
    TestServer.start()


def teardown_package():
    TestServer.stop()


@attr('feature')
class BrowserTest(TestCase):
    def setUp(self):
        self.browser = Browser('phantomjs', wait_time=3)

    def tearDown(self):
        self.browser.quit()

