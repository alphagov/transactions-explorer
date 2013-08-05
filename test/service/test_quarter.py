import unittest
from hamcrest import assert_that, is_, less_than, greater_than, equal_to
from lib.service import Quarter


class TestQuarter(unittest.TestCase):
    def test_string_conversion(self):
        q = Quarter(2013, 1)

        s = "%s" % q

        assert_that(s, is_("Q1 2013"))

    def test_parse_from_string(self):
        quarter = Quarter.parse("2013_q2")

        assert_that(quarter.year, is_(2013))
        assert_that(quarter.quarter, is_(2))

    def test_comparison(self):
        q2_2013 = Quarter.parse("2013_q2")
        q1_2013 = Quarter.parse("2013_q1")
        q4_2012 = Quarter.parse("2012_q4")

        assert_that(q4_2012, is_(less_than(q1_2013)))
        assert_that(q1_2013, is_(less_than(q2_2013)))
        assert_that(q1_2013, is_(greater_than(q4_2012)))
        assert_that(q2_2013, is_(greater_than(q1_2013)))
        assert_that(q2_2013, is_(equal_to(q2_2013)))
