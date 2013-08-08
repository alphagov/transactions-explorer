import unittest
from hamcrest import is_, assert_that
from lib.service import Department, Service
from test.service import details


class TestDepartment(unittest.TestCase):

    def test_department_creation(self):
        d = Department("Agengy for Beatiful Code", [])
        assert_that(d.name, is_("Agengy for Beatiful Code"))

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
