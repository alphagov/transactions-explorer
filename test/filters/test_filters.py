from hamcrest import assert_that, is_
from lib.filters import number_as_magnitude, number_as_financial_magnitude


def test_number_as_magnitude():
    assert_that(number_as_magnitude(1.23),  is_("1.23"))
    assert_that(number_as_magnitude(1.234), is_("1.23"))
    assert_that(number_as_magnitude(1.236), is_("1.24"))

    assert_that(number_as_magnitude(12.3),  is_("12.3"))
    assert_that(number_as_magnitude(12.34), is_("12.3"))
    assert_that(number_as_magnitude(12.36), is_("12.4"))

    assert_that(number_as_magnitude(123),   is_("123"))
    assert_that(number_as_magnitude(123.4), is_("123"))
    assert_that(number_as_magnitude(123.6), is_("124"))

    assert_that(number_as_magnitude(1230), is_("1.23k"))
    assert_that(number_as_magnitude(1234), is_("1.23k"))
    assert_that(number_as_magnitude(1236), is_("1.24k"))

    assert_that(number_as_magnitude(12300), is_("12.3k"))
    assert_that(number_as_magnitude(12340), is_("12.3k"))
    assert_that(number_as_magnitude(12360), is_("12.4k"))

    assert_that(number_as_magnitude(123000), is_("123k"))
    assert_that(number_as_magnitude(123400), is_("123k"))
    assert_that(number_as_magnitude(123600), is_("124k"))

    assert_that(number_as_magnitude(1230000), is_("1.23m"))
    assert_that(number_as_magnitude(1234000), is_("1.23m"))
    assert_that(number_as_magnitude(1236000), is_("1.24m"))

    assert_that(number_as_magnitude(12300000), is_("12.3m"))
    assert_that(number_as_magnitude(12340000), is_("12.3m"))
    assert_that(number_as_magnitude(12360000), is_("12.4m"))

    assert_that(number_as_magnitude(123000000), is_("123m"))
    assert_that(number_as_magnitude(123400000), is_("123m"))
    assert_that(number_as_magnitude(123600000), is_("124m"))

    assert_that(number_as_magnitude(1230000000), is_("1.23bn"))
    assert_that(number_as_magnitude(1234000000), is_("1.23bn"))
    assert_that(number_as_magnitude(1236000000), is_("1.24bn"))

    assert_that(number_as_magnitude(12300000000), is_("12.3bn"))
    assert_that(number_as_magnitude(12340000000), is_("12.3bn"))
    assert_that(number_as_magnitude(12360000000), is_("12.4bn"))

    assert_that(number_as_magnitude(123000000000), is_("123bn"))
    assert_that(number_as_magnitude(123400000000), is_("123bn"))
    assert_that(number_as_magnitude(123600000000), is_("124bn"))


def test_number_as_financial_magnitude():
    assert_that(number_as_financial_magnitude(1.23),  is_("1.23"))
    assert_that(number_as_financial_magnitude(1.234), is_("1.23"))
    assert_that(number_as_financial_magnitude(1.236), is_("1.24"))

    assert_that(number_as_financial_magnitude(12.33),  is_("12.33"))
    assert_that(number_as_financial_magnitude(12.334), is_("12.33"))
    assert_that(number_as_financial_magnitude(12.336), is_("12.34"))

    assert_that(number_as_financial_magnitude(123),   is_("123"))
    assert_that(number_as_financial_magnitude(123.4), is_("123"))
    assert_that(number_as_financial_magnitude(123.6), is_("124"))

    assert_that(number_as_financial_magnitude(1230), is_("1.23k"))
    assert_that(number_as_financial_magnitude(1234), is_("1.23k"))
    assert_that(number_as_financial_magnitude(1236), is_("1.24k"))

    assert_that(number_as_financial_magnitude(12300), is_("12.3k"))
    assert_that(number_as_financial_magnitude(12340), is_("12.3k"))
    assert_that(number_as_financial_magnitude(12360), is_("12.4k"))

    assert_that(number_as_financial_magnitude(123000), is_("123k"))
    assert_that(number_as_financial_magnitude(123400), is_("123k"))
    assert_that(number_as_financial_magnitude(123600), is_("124k"))

    assert_that(number_as_financial_magnitude(1230000), is_("1.23m"))
    assert_that(number_as_financial_magnitude(1234000), is_("1.23m"))
    assert_that(number_as_financial_magnitude(1236000), is_("1.24m"))

    assert_that(number_as_financial_magnitude(12300000), is_("12.3m"))
    assert_that(number_as_financial_magnitude(12340000), is_("12.3m"))
    assert_that(number_as_financial_magnitude(12360000), is_("12.4m"))

    assert_that(number_as_financial_magnitude(123000000), is_("123m"))
    assert_that(number_as_financial_magnitude(123400000), is_("123m"))
    assert_that(number_as_financial_magnitude(123600000), is_("124m"))

    assert_that(number_as_financial_magnitude(1230000000), is_("1.23bn"))
    assert_that(number_as_financial_magnitude(1234000000), is_("1.23bn"))
    assert_that(number_as_financial_magnitude(1236000000), is_("1.24bn"))

    assert_that(number_as_financial_magnitude(12300000000), is_("12.3bn"))
    assert_that(number_as_financial_magnitude(12340000000), is_("12.3bn"))
    assert_that(number_as_financial_magnitude(12360000000), is_("12.4bn"))

    assert_that(number_as_financial_magnitude(123000000000), is_("123bn"))
    assert_that(number_as_financial_magnitude(123400000000), is_("123bn"))
    assert_that(number_as_financial_magnitude(123600000000), is_("124bn"))
