from hamcrest import *
from nose.tools import nottest

from test.features import BrowserTest


class GenerateDepartmentPages(BrowserTest):

    def test_generates_department_title(self):
        self.browser.visit("http://0.0.0.0:8000/department/def")
        title = self.browser.find_by_css('#whitehall-wrapper').text

        assert_that(title, is_(u'Department of Electronic Freedom'))


