from hamcrest import *

from test.features import BrowserTest
from test.features.support import table_from


class Javascript(BrowserTest):

    def test_all_services_table(self):
        self.browser.visit("http://0.0.0.0:8000/SpecRunner")
        tests_passing = self.browser.find_by_css('.symbolSummary .passed')
        tests_failing = self.browser.find_by_css('.symbolSummary .failed')

        print 'Tests passing %s' % len(tests_passing)
        print 'Tests failing %s' % len(tests_failing)

        assert_that(len(tests_failing), is_(0))
