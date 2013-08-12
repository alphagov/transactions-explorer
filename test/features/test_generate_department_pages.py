from hamcrest import *
from nose.tools import nottest

from test.features import BrowserTest


class GenerateDepartmentPages(BrowserTest):

    def test_generates_title(self):
        self.browser.visit("http://0.0.0.0:8000/department/def")
        title = self.browser.find_by_css('#whitehall-wrapper').text

        assert_that(title, is_(u'Department of Electronic Freedom'))

    def test_generate_data_coverage(self):
        self.browser.visit("http://0.0.0.0:8000/department/abc")
        coverage = self.browser.find_by_css('#data-coverage-notice').text

        assert_that(coverage, is_(u'Department data coverage: 66.7%\n(taken from 1 high volume services)'))

    def test_do_not_generate_data_coverage_if_no_high_volume_services(self):
        self.browser.visit("http://0.0.0.0:8000/department/low")

        assert_that(self.browser.is_element_not_present_by_css('#data-coverage-notice'),
                    is_(True))

