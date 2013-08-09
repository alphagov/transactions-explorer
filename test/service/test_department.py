import unittest
from hamcrest import is_, assert_that, contains, close_to
from lib.service import Department, Service
from test.service import details


class TestDepartment(unittest.TestCase):

    def test_department_creation(self):
        d = Department("Agengy for Beatiful Code", [])
        assert_that(d.name, is_("Agengy for Beatiful Code"))

    def test_building_a_list_of_departments_from_services(self):
        services = [
            Service(details({u'Abbr': 'ABC', u'Department': "Agency for Beautiful Code"})),
            Service(details({u'Abbr': 'MSW', u'Department': "Ministry of Silly Walks"})),
            Service(details({u'Abbr': 'ABC', u'Department': "Agency for Beautiful Code"})),
        ]

        departments = Department.from_services(services)

        assert_that(len(departments), is_(2))
        assert_that(departments[0].name, is_("Agency for Beautiful Code"))
        assert_that(departments[0].services,
                    contains(services[0], services[2]))

    def test_volume_is_total_of_last_available_quarter_for_each_service(self):
        services = [
            Service(details({"2012-Q4 Vol.": "1,000", "2013-Q1 Vol.": "1,500"})),
            Service(details({"2012-Q4 Vol.": "2,000"})),
        ]

        dept = Department("Agengy for Beatiful Code", services)

        assert_that(dept.volume, is_(3500))


    def test_volume_with_one_service(self):
        services = [
            Service(details({"2012-Q4 Vol.": "2,000"}))
        ]

        dept = Department("Agengy for Beatiful Code", services)

        assert_that(dept.volume, is_(2000))

    def test_volume_ignores_services_with_no_kpis(self):
        services = [
            Service(details({"2012-Q4 Vol.": "2,000"})),
            Service(details({})),
        ]

        dept = Department("Agengy for Beatiful Code", services)

        assert_that(dept.volume, is_(2000))

    def test_volume_is_none_if_no_service_has_kpis(self):
        services = [
            Service(details({})),
        ]

        dept = Department("Agengy for Beatiful Code", services)

        assert_that(dept.volume, is_(None))

    def test_cost_is_sum_of_transaction_costs_for_each_transaction_handled(self):
        services = [
            Service(details({
                "2012-Q4 Vol.": "2,000",
                u'2012-Q4 CPT (\xa3)': "2.00",
                u'High-volume?': 'yes'
            })),
            Service(details({
                "2013-Q1 Vol.": "1,000",
                u'2013-Q1 CPT (\xa3)': "3.00",
                u'High-volume?': 'yes'
            })),
        ]

        dept = Department("Agengy for Beatiful Code", services)

        assert_that(dept.cost, is_(7000))

    def test_cost_ignores_non_high_volume_services(self):
        services = [
            Service(details({
                "2012-Q4 Vol.": "2,000",
                u'2012-Q4 CPT (\xa3)': "2.00",
                u'High-volume?': 'yes'
            })),
            Service(details({
                "2013-Q1 Vol.": "1,000",
                u'2013-Q1 CPT (\xa3)': "3.00",
            })),
        ]

        dept = Department("Agengy for Beatiful Code", services)

        assert_that(dept.cost, is_(4000))

    def test_cost_is_none_when_no_high_volume_services(self):
        services = [
            Service(details({
                "2012-Q4 Vol.": "2,000",
                u'2012-Q4 CPT (\xa3)': "2.00",
            })),
            Service(details({
                "2013-Q1 Vol.": "1,000",
                u'2013-Q1 CPT (\xa3)': "3.00",
            })),
        ]

        dept = Department("Agengy for Beatiful Code", services)

        assert_that(dept.cost, is_(None))

    def test_cost_ignores_services_with_no_cpt(self):
        services = [
            Service(details({
                "2012-Q4 Vol.": "2,000",
                u'High-volume?': 'yes'
            })),
            Service(details({
                "2013-Q1 Vol.": "1,000",
                u'2013-Q1 CPT (\xa3)': "3.00",
                u'High-volume?': 'yes'
            })),
        ]

        dept = Department("Agengy for Beatiful Code", services)

        assert_that(dept.cost, is_(3000))

    def test_cost_is_none_when_no_kpi_is_available(self):
        services = [
            Service(details({
                u'High-volume?': 'yes'
            })),
            Service(details({
                u'High-volume?': 'yes'
            })),
        ]

        dept = Department("Agengy for Beatiful Code", services)

        assert_that(dept.cost, is_(None))

    def test_takeup_is_volume_divided_by_digital_volume(self):
        services = [
            Service(details({
                '2012-Q4 Vol.': '10',
                '2012-Q4 Digital vol.': '5',
                u'High-volume?': 'yes'
            })),
            Service(details({
                '2012-Q4 Vol.': '30',
                '2012-Q4 Digital vol.': '10',
                u'High-volume?': 'yes'
            })),
        ]

        dept = Department("Agengy for Beatiful Code", services)

        assert_that(dept.takeup, is_(0.375))

    def test_takeup_is_none_if_digital_volume_is_none(self):
        services = [
            Service(details({
                '2012-Q4 Vol.': '10',
                u'High-volume?': 'yes'
            })),
            Service(details({
                '2012-Q4 Vol.': '30',
                u'High-volume?': 'yes'
            })),
        ]

        dept = Department("Agengy for Beatiful Code", services)

        assert_that(dept.takeup, is_(None))

    def test_takeup_is_none_if_volume_is_none(self):
        services = [
            Service(details({
                '2012-Q4 Digital vol.': '5',
                u'High-volume?': 'yes'
            })),
            Service(details({
                '2012-Q4 Digital vol.': '10',
                u'High-volume?': 'yes'
            })),
        ]

        dept = Department("Agengy for Beatiful Code", services)

        assert_that(dept.takeup, is_(None))

    def test_takeup_only_includes_high_volume_services(self):
        services = [
            Service(details({
                '2012-Q4 Vol.': '10',
                '2012-Q4 Digital vol.': '5',
                u'High-volume?': 'yes'
            })),
            Service(details({
                '2012-Q4 Vol.': '30',
                '2012-Q4 Digital vol.': '10',
                u'High-volume?': 'yes'
            })),
            Service(details({
                '2012-Q4 Vol.': '30',
                '2012-Q4 Digital vol.': '10',
            })),
        ]

        dept = Department("Agengy for Beatiful Code", services)

        assert_that(dept.takeup, is_(0.375))

    def test_takeup_use_data_from_the_same_quarter_for_volume_and_digital_volume(self):
        services = [
            Service(details({
                '2012-Q4 Vol.': '10',
                '2012-Q4 Digital vol.': '5',
                u'High-volume?': 'yes'
            })),
            Service(details({
                '2012-Q4 Vol.': '30',
                '2012-Q4 Digital vol.': '10',
                '2013-Q1 Vol.': '20',
                u'High-volume?': 'yes'
            })),
        ]

        dept = Department("Agengy for Beatiful Code", services)

        assert_that(dept.takeup, is_(0.375))

    def test_cost_use_data_from_the_same_quarter_for_volume_and_digital_volume(self):
        services = [
            Service(details({
                "2012-Q4 Vol.": "2,000",
                u'2012-Q4 CPT (\xa3)': "2.00",
                u'High-volume?': 'yes'
            })),
            Service(details({
                "2012-Q4 Vol.": "1,000",
                u'2012-Q4 CPT (\xa3)': "3.00",
                "2013-Q1 Vol.": "3,000",
                u'High-volume?': 'yes'
            })),
        ]

        dept = Department("Agengy for Beatiful Code", services)

        assert_that(dept.cost, is_(7000))

    def test_data_coverage_is_average_of_service_coverages(self):
        services = [
            #66.66
            Service(details({
                "2012-Q4 Vol.": "2,000",
                '2012-Q4 Digital vol.': '10',
                u'2012-Q4 CPT (\xa3)': "2.00",
                "2013-Q1 Vol.": "2,000",
                u'2013-Q1 CPT (\xa3)': "2.00",
                '2013-Q1 Digital vol.': '10',
                u'High-volume?': 'yes'
            })),
            #33.33
            Service(details({
                "2012-Q4 Vol.": "1,000",
                u'2012-Q4 CPT (\xa3)': "3.00",
                '2012-Q4 Digital vol.': '10',
                u'High-volume?': 'yes'
            })),
        ]

        dept = Department("Agengy for Beatiful Code", services)

        assert_that(dept.data_coverage, is_(0.5))

    def test_data_coverage_excludes_non_high_volume_services(self):
        services = [
            #66.66
            Service(details({
                "2012-Q4 Vol.": "2,000",
                '2012-Q4 Digital vol.': '10',
                u'2012-Q4 CPT (\xa3)': "2.00",
                "2013-Q1 Vol.": "2,000",
                u'2013-Q1 CPT (\xa3)': "2.00",
                '2013-Q1 Digital vol.': '10',
            })),
            #33.33
            Service(details({
                "2012-Q4 Vol.": "1,000",
                u'2012-Q4 CPT (\xa3)': "3.00",
                '2012-Q4 Digital vol.': '10',
                u'High-volume?': 'yes'
            })),
        ]

        dept = Department("Agengy for Beatiful Code", services)

        assert_that(dept.data_coverage, close_to(0.3333, 0.001))

    def test_data_coverage_is_none_when_no_high_volume_services(self):
        services = [
            #66.66
            Service(details({
                "2012-Q4 Vol.": "2,000",
                '2012-Q4 Digital vol.': '10',
                u'2012-Q4 CPT (\xa3)': "2.00",
                "2013-Q1 Vol.": "2,000",
                u'2013-Q1 CPT (\xa3)': "2.00",
                '2013-Q1 Digital vol.': '10',
            })),
            #33.33
            Service(details({
                "2012-Q4 Vol.": "1,000",
                u'2012-Q4 CPT (\xa3)': "3.00",
                '2012-Q4 Digital vol.': '10',
            })),
        ]

        dept = Department("Agengy for Beatiful Code", services)

        assert_that(dept.data_coverage, is_(None))

