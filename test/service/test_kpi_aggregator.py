import unittest
from hamcrest import is_, assert_that
from lib.service import Department, Service, ServiceKpiAggregator
from test.service import details


class TestServiceKpiAggregator(unittest.TestCase):

    def test_aggregate_is_sum_of_values_when_high_volume_does_not_matter(self):
        services = [
            Service(details({"2012-Q4 Vol.": "2,000"})),
            Service(details({"2012-Q4 Vol.": "3,000"})),
        ]

        kpi_aggregator = ServiceKpiAggregator(services)

        assert_that(kpi_aggregator.aggregate('volume_num'), is_(5000))

    def test_aggregate_is_sum_of_values_when_high_volume_matters(self):
        services = [
            Service(details({"2012-Q4 Vol.": "2,000", u'High-volume?': 'yes'})),
            Service(details({"2012-Q4 Vol.": "3,000"}))
        ]

        kpi_aggregator = ServiceKpiAggregator(services)

        assert_that(kpi_aggregator.aggregate('volume_num', high_volume_only=True), is_(2000))

    def test_aggregate_is_none_when_no_high_volume_services_and_ignore_non_high_volume(self):
        services = [
            Service(details({"2012-q4 vol.": "2,000"})),
            Service(details({"2012-q4 vol.": "3,000"}))
        ]

        kpi_aggregator = ServiceKpiAggregator(services)

        assert_that(kpi_aggregator.aggregate('volume_num', high_volume_only=True), is_(None))

    def test_aggregate_is_none_when_no_kpis(self):
        services = [
            Service(details({})),
        ]

        kpi_aggregator = ServiceKpiAggregator(services)

        assert_that(kpi_aggregator.aggregate('volume_num'), is_(None))

    def test_aggregate_ignores_when_no_kpis(self):
        services = [
            Service(details({"2012-Q4 Vol.": "2,000"})),
            Service(details({})),
        ]

        kpi_aggregator = ServiceKpiAggregator(services)

        assert_that(kpi_aggregator.aggregate('volume_num'), is_(2000))

    def test_aggregate_is_none_when_no_values(self):
        services = [
            Service(details({u'2012-Q4 Digital vol.': "2,000"})),
            Service(details({u'2012-Q4 Digital vol.': "3,000"}))
        ]

        kpi_aggregator = ServiceKpiAggregator(services)

        assert_that(kpi_aggregator.aggregate('volume_num'), is_(None))
    
