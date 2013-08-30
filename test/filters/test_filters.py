from hamcrest import assert_that, is_
from lib.filters import number_as_magnitude, number_as_financial_magnitude, join_url_parts, string_as_static_url, digest, number_as_grouped_number, number_as_percentage_change


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


def test_number_as_grouped_number():
    assert_that(number_as_grouped_number(123456789), is_("123,456,789"))
    assert_that(number_as_grouped_number(123), is_("123"))

    assert_that(number_as_grouped_number(4567.22), is_("4,567"))
    assert_that(number_as_grouped_number(4567.98), is_("4,568"))

    assert_that(number_as_grouped_number("not a number"), is_(""))


def test_number_as_percentage_change():
    assert_that(number_as_percentage_change(None), is_("0%"))
    assert_that(number_as_percentage_change(1.0), is_("0%"))
    assert_that(number_as_percentage_change(1.00001), is_("0%"))
    assert_that(number_as_percentage_change(0.999991), is_("0%"))

    assert_that(number_as_percentage_change(0.0), is_("-100%"))
    assert_that(number_as_percentage_change(2.0), is_("+100%"))

    assert_that(number_as_percentage_change(1.1234567), is_("+12.35%"))
    assert_that(number_as_percentage_change(0.1234567), is_("-87.65%"))

class Test_join_url_parts(object):
    def test_string_as_link(self):
        assert_that(
            join_url_parts('/', 'some/path'),
            is_('/some/path'))

    def test_string_as_link_with_user_defined_path_prefix(self):
        assert_that(
            join_url_parts('/custom/prefix/', 'some/path'),
            is_('/custom/prefix/some/path'))

    def test_string_as_link_adds_trailing_slash_after_prefix(self):
        assert_that(
            join_url_parts('/custom/prefix', 'some/path'),
            is_('/custom/prefix/some/path'))

    def test_string_as_link_does_not_add_double_slashes(self):
        assert_that(
            join_url_parts('/custom/prefix/', '/some/path'),
            is_('/custom/prefix/some/path'))


class Test_string_as_static_url:
    def setUp(self):
        digest.set_digests({})

    def test_return_url_with_digest(self):
        digest.set_digests({
            'asset.css': 'asset-1425361275412.css'
        })
        assert_that(
            string_as_static_url('asset.css'),
            is_('https://assets.digital.cabinet-office.gov.uk/static/asset-1425361275412.css')
        )

    def test_fallback_to_plain_url_when_digest_is_unknown(self):
        assert_that(
            string_as_static_url('asset.css'),
            is_('https://assets.digital.cabinet-office.gov.uk/static/asset.css')
        )
