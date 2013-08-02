import unittest
from hamcrest import assert_that, is_
from lib.service import Service


keys = [
 u'FOI text',
 u'Latest cost per transaction',
 u'Department',
 u'2013-Q3 User satisfaction',
 u'2013-Q3 Vol.',
 u'Notes [for GDS only]',
 u'2013-Q2 Completion rate',
 u'FOI data',
 u'2013-Q1 User satisfaction',
 u'URL',
 u'2014-Q2 CPT (\xa3)',
 u'2012-Q4 Completion rate',
 u'GOV.UK start page',
 u'2012-Q4 User satisfaction',
 u'2014-Q3 Completion rate',
 u'Business model',
 u'High-volume?',
 u'2012Q4 take-up',
 u'2013-Q4 CPT (\xa3)',
 u'Latest volumes',
 u'2014-Q2 Vol.',
 u'2014-Q2 Completion rate',
 u'2014-Q1 User satisfaction',
 u'2014-Q2 User satisfaction',
 u'Latest digital take-up',
 u'FOI URL',
 u'2012-Q4 CPT (\xa3)',
 u'2013-Q4 Digital vol.',
 u'Data coverage \n(i.e. how many of 3 key data sets we have)',
 u'Abbr',
 u'Other notes',
 u'2013-Q4 Vol.',
 u'No of electronic transactions',
 u'2013-Q2 CPT (\xa3)',
 u'2013-Q2 Vol.',
 u'2013-Q1 Completion rate',
 u'2014-Q1 Digital vol.',
 u'2013-Q1 Digital vol.',
 u'2012-Q4 Digital vol.',
 u'Total cost',
 u'2014-Q4 Vol.',
 u'2014-Q2 Digital CPT (\xa3)',
 u'2014-Q1 Digital CPT (\xa3)',
 u'2014-Q4 User satisfaction',
 u'Category',
 u'CPT difference',
 u'Agency/body',
 u'2014-Q4 Digital vol.',
 u'Cumulative',
 u'2013-Q3 Completion rate',
 u'2013-Q3 Digital vol.',
 u'Take-up difference',
 u'2014-Q1 Completion rate',
 u'2014-Q3 Digital CPT (\xa3)',
 u'Percentage digital take-up\n2012 Q4',
 u'2013-Q4 Digital CPT (\xa3)',
 u'Customer type',
 u'2013-Q2 Digital vol.',
 u'2013-Q2 User satisfaction',
 u'2014-Q3 CPT (\xa3)',
 u'2012-Q4 Vol.',
 u'Percentage digital take-up\n2013 Q1',
 u'No of web transactions',
 u'2014-Q2 Digital vol.',
 u'Short service name',
 u'2014-Q1 Vol.',
 u'2014-Q3 User satisfaction',
 u'Keywords',
 u'2013-Q3 Digital CPT (\xa3)',
 u'2014-Q4 Digital CPT (\xa3)',
 u'Description of service',
 u'2014-Q4 CPT (\xa3)',
 u'Name of service',
 u'2013Q1 take-up',
 u'2014-Q3 Vol.',
 u'2013-Q4 User satisfaction',
 u'Notes on costs',
 u'2012-Q4 Digital CPT (\xa3)',
 u'2013-Q1 Digital CPT (\xa3)',
 u'Latest digital total',
 u'Detailed view?',
 u'2013-Q4 Completion rate',
 u'2013-Q1 CPT (\xa3)',
 u'2013-Q3 CPT (\xa3)',
 u'2014-Q4 Completion rate',
 u'2014-Q1 CPT (\xa3)',
 u'Agency abbr',
 u'2013-Q1 Vol.',
 u'2014-Q3 Digital vol.',
 u'2013-Q2 Digital CPT (\xa3)']


row_defaults = dict( [ (key, None) for key in keys ] )

def row(values):
    return dict( [ (key, values.get(key)) for key in keys ] )


class TestService(unittest.TestCase):
    def test_slug(self):
        service = Service(row({'Abbr': 'abc',
                               'Name of service': 'Add Beautiful Code'}))

        assert_that(service.slug, is_('abc-add-beautiful-code'))

    def test_link(self):
        service = Service(row({'Abbr': 'abc',
                               'Name of service': 'Add Beautiful Code'}))

        assert_that(service.link,
                    is_('service-details/abc-add-beautiful-code.html'))

