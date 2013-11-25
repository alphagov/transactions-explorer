import unittest
from datetime import date
from hamcrest import assert_that, is_, less_than, greater_than, equal_to
from lib.service import Quarter


class TestQuarter(unittest.TestCase):
    def test_string_conversion_default(self):
        assert_that("%s" % Quarter(2013, 1), is_("Jan 2012 to Dec 2012"))
        assert_that("%s" % Quarter(2013, 2), is_("Apr 2012 to Mar 2013"))
        assert_that("%s" % Quarter(2013, 3), is_("July 2012 to June 2013"))

    def test_string_conversion_q4_2012_exception(self):
        assert_that("%s" % Quarter(2012, 4), is_("Apr 2011 to Mar 2012"))

    def test_format_date(self):
        assert_that(Quarter.format_date(date(2013, 1, 1)), is_("Jan 2013"))
        assert_that(Quarter.format_date(date(2013, 2, 1)), is_("Feb 2013"))
        assert_that(Quarter.format_date(date(2013, 3, 1)), is_("Mar 2013"))
        assert_that(Quarter.format_date(date(2013, 4, 1)), is_("Apr 2013"))
        assert_that(Quarter.format_date(date(2013, 5, 1)), is_("May 2013"))
        assert_that(Quarter.format_date(date(2013, 6, 1)), is_("June 2013"))
        assert_that(Quarter.format_date(date(2013, 7, 1)), is_("July 2013"))
        assert_that(Quarter.format_date(date(2013, 8, 1)), is_("Aug 2013"))
        assert_that(Quarter.format_date(date(2013, 9, 1)), is_("Sept 2013"))
        assert_that(Quarter.format_date(date(2013, 10, 1)), is_("Oct 2013"))
        assert_that(Quarter.format_date(date(2013, 11, 1)), is_("Nov 2013"))
        assert_that(Quarter.format_date(date(2013, 12, 1)), is_("Dec 2013"))

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
