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

