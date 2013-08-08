import unittest
from hamcrest import assert_that, is_
from lib.service import Service
from test.service import details


class TestService(unittest.TestCase):
    def test_slug(self):
        service = Service(details({'Abbr': 'abc',
                                   'Name of service': 'Add Beautiful Code'}))

        assert_that(service.slug, is_('abc-add-beautiful-code'))

    def test_link(self):
        service = Service(details({'Abbr': 'abc',
                                   'Name of service': 'Add Beautiful Code'}))

        assert_that(service.link,
                    is_('service-details/abc-add-beautiful-code.html'))

    def test_zero_volumes(self):
        service = Service(details({'2012-Q4 Vol.': '0',
                                   '2012-Q4 Digital vol.': '0'}))

        assert_that(service.most_recent_kpis['takeup'],
                    is_(None))

    def test_volumes(self):
        service = Service(details({'2012-Q4 Vol.': '10',
                                   '2012-Q4 Digital vol.': '5'}))

        assert_that(service.most_recent_kpis['takeup'],
                    is_(.5))

    def test_no_kpis(self):
        service = Service(details({}))

        assert_that(service.most_recent_kpis,
                    is_(None))


