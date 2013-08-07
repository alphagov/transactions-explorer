import unittest
from hamcrest import is_, assert_that
from lib.service import Department


class TestDepartment(unittest.TestCase):

    def test_department_creation(self):

        d = Department("Agengy for Beatiful Code", [])

        assert_that(d.name, is_("Agengy for Beatiful Code"))