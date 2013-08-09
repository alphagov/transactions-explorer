import unittest
from hamcrest.core import *
from lib.csv import tabular_map
from lib.service import Service
from test.service import details


class TestCSV(unittest.TestCase):
    def test_csv_generation(self):
        services = [
            Service(details({"Name of service": "test_name", "Abbr": "tn"})),
            Service(details({"Name of service": "test_name_2", "Abbr": "tn2"}))
        ]

        table = tabular_map([("name_column", lambda s: s.name),
                            ("abbr", lambda s: s.abbr)],
                            services)

        assert_that(table, is_([["name_column", "abbr"],
                                ["test_name", "tn"],
                                ["test_name_2", "tn2"]]))

    def test_strings_get_utf8_encoded(self):
        services = [Service(details({"Name of service": u"\u2019"}))]

        table = tabular_map([("column", lambda s: s.name)], services)

        assert_that(table, is_([["column"], ["\xe2\x80\x99"]]))