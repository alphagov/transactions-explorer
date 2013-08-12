from hamcrest import *

from test.features import BrowserTest
from test.features.support import table_from


class GenerateHighVolumeServicesPages(BrowserTest):

    def test_all_services_table(self):
        self.browser.visit("http://0.0.0.0:8000/high-volume-services/by-transactions-per-year/descending.html")
        table = table_from(self.browser.find_by_css('tbody tr'))

        assert_that(table, is_([
            [u'Service 4', u'DEF', u'\xa312.1m*', u'\xa31.30*', u'94.8%*', u'9,321,067*'],
            [u'Service 1', u'ABC', u'\xa3482k', u'\xa30.10', u'100%', u'4,820,000'],
            [u'Service 5', u'DEF', u'\xa313.1m*', u'\xa33.40*', u'100%*', u'3,847,098*'],
            [u'Service 6', u'DEF', u'\xa341.9m*', u'\xa312.30*', u'30%*', u'3,404,261*'],
            [u'Service 7', u'DEF', u'\xa381.1m', u'\xa334.40', u'97.6%', u'2,358,738'],
            [u'Service 8', u'DEF', u'\xa39.25m', u'\xa34.23', u'86%', u'2,186,450']
        ]))
