from pprint import pprint
import unittest
from hamcrest import assert_that, is_, close_to
from lib.service import Service, total_transaction_volume
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

        assert_that(service.most_recent_kpis['takeup'], is_(0.5))
 
    def test_most_recent_kpi_takeup_is_none_if_no_matching_quarters(self):
        service = Service(details({'2012-Q4 Vol.': '10',
                                   '2013-Q1 Digital vol.': '5'}))

        assert_that(service.most_recent_kpis['takeup'],
                    is_(None))

    def test_no_kpis(self):
        service = Service(details({}))

        assert_that(service.most_recent_kpis,
                    is_(None))

    def test_no_kpi_for_quarter_with_noVolume(self):
        service = Service(details({
           '2012-Q4 Digital vol.': '5'
        }))

        assert_that(service.most_recent_kpis,
                    is_(None))

    def test_most_recent_kpi_with_given_attribute(self):
        service = Service(details({
            '2012-Q4 Vol.': '10',
            '2012-Q4 Digital vol.': '5',
            '2013-Q1 Vol.': '3',
        }))

        assert_that(service.most_recent_kpis_with(['volume_num', 'digital_volume_num'])['volume_num'],
                    is_(10))

    def test_most_recent_kpi_with_attributes_are_none_if_no_attributes_are_present(self):
        service = Service(details({
            '2012-Q4 Vol.': '10',
            '2013-Q1 Vol.': '3',
        }))

        assert_that(service.most_recent_kpis_with(['volume_num', 'digital_volume_num']),
                    is_(None))


    def test_cost(self):
        service = Service(details({
            "2012-Q4 Vol.": "2,000",
            u'2012-Q4 CPT (\xa3)': "2.00"
        }))

        pprint(service.most_recent_kpis)

        assert_that(service.most_recent_kpis['cost'], is_(4000))

    def test_cost_is_non_when_no_cpt(self):
        service = Service(details({
            "2012-Q4 Vol.": "2,000",
        }))

        pprint(service.most_recent_kpis)

        assert_that(service.most_recent_kpis['cost'], is_(None))

    def test_transactions_count(self):
        service = Service(details({'2013-Q1 Vol.': '10'}))

        assert_that(service.most_recent_kpis['volume_num'], is_(10))

    def test_coverage(self):
        service = Service(details({
            "2012-Q4 Vol.": "2,000",
            '2012-Q4 Digital vol.': '10',
            u'2012-Q4 CPT (\xa3)': "2.00",
            "2013-Q1 Vol.": "2,000",
            u'2013-Q1 CPT (\xa3)': "2.00",
            '2013-Q1 Digital vol.': '10',
            u'High-volume?': 'yes'
        }))

        assert_that(float(service.data_coverage), close_to(0.6667, 0.001))

    def test_most_up_to_date_volume(self):
        service_with_one_vol = Service(details({'2013-Q1 Vol.': '200'}))
        service_with_two_vols = Service(details({'2013-Q1 Vol.': '200',
                                                 '2013-Q2 Vol.': '250'}))
        service_with_no_vols = Service(details({}))

        assert_that(service_with_one_vol.most_up_to_date_volume, is_(200))
        assert_that(service_with_two_vols.most_up_to_date_volume, is_(250))
        assert_that(service_with_no_vols.most_up_to_date_volume, is_(None))

    def test_keywords(self):
        service_with_no_keywords = Service(details({'Keywords': None}))
        service_with_one_keywords = Service(details({'Keywords': 'keyword'}))
        service_with_two_keywords = Service(details({'Keywords': 'keyword1, keyword2'}))

        assert_that(service_with_no_keywords.keywords, is_([]))
        assert_that(service_with_one_keywords.keywords, is_(['keyword']))
        assert_that(service_with_two_keywords.keywords, is_(['keyword1', 'keyword2']))

    def test_agency_abbr_if_supplied(self):
        service = Service(details({
            "Agency/body": "A and B and C",
            "Agency abbr": "ABC",
        }))

        assert_that(service.agency_abbreviation, is_("ABC"))

    def test_agency_abbr_is_full_name_if_not_supplied(self):
        service = Service(details({
            "Agency/body": "A and B and C",
            "Agency abbr": "",
        }))

        assert_that(service.agency_abbreviation, is_("A and B and C"))


class TestSummingTotalTransactions(unittest.TestCase):

    def test_sum_of_total_transactions(self):
        services = [Service(details({'2013-Q1 Vol.': '10'})),
                    Service(details({'2013-Q2 Vol.': '20'})),
                    Service(details({'2013-Q1 Vol.': '30'}))]

        assert_that(total_transaction_volume(services), is_(60))

    def test_sum_of_total_transactions_when_kpis_are_missing(self):
        services = [Service(details({})),
                    Service(details({'2013-Q2 Vol.': '100'}))]

        assert_that(services[0].has_kpis, is_(False))
        assert_that(total_transaction_volume(services), is_(100))
