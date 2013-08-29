from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import locale

from re import sub
from lib.filters import digest


NO_DECIMAL_PLACE = Decimal('1')
ONE_DECIMAL_PLACE = Decimal('0.1')
TWO_DECIMAL_PLACES = Decimal('0.01')


locale.setlocale(locale.LC_ALL, 'en_GB.utf-8')

path_prefix = '/'
asset_prefix = '/transactions-explorer/'
static_prefix = 'https://assets.digital.cabinet-office.gov.uk/static'


def as_number(num):
    if num:
        just_numbers = sub(r'[^\d\.]+', '', num)
        try:
            return Decimal(just_numbers)
        except InvalidOperation:
            pass
    return None


def _reduce_to_magnitude(num):
    if num > 1000000000:
        return num / 1000000000, "bn"
    if num > 1000000:
        return num / 1000000, "m"
    if num > 1000:
        return num / 1000, "k"
    return num, ""


def _precision(num):
    if num < 10:
        return TWO_DECIMAL_PLACES
    elif num < 100:
        return ONE_DECIMAL_PLACE
    return NO_DECIMAL_PLACE


def _round(num, precision):
    return num.quantize(precision, rounding=ROUND_HALF_UP)


def number_as_magnitude(num):
    if num is None:
        return 0
    if isinstance(num, basestring):
        num = as_number(num)
    if type(num) is not Decimal:
        num = Decimal(num)

    num, suffix = _reduce_to_magnitude(num)
    return "%s%s" % (_round(num, _precision(num)), suffix)


def number_as_financial_magnitude(num):
    if num is None:
        return 0
    if isinstance(num, basestring):
        num = as_number(num)
    if type(num) is not Decimal:
        num = Decimal(num)

    reduced, suffix = _reduce_to_magnitude(num)

    if num < 100:
        precision = TWO_DECIMAL_PLACES
    else:
        precision = _precision(reduced)

    return "%s%s" % (_round(reduced, precision), suffix)


def number_as_percentage(num):
    if isinstance(num, basestring):
        num = as_number(num)

    if num is None:
        return ''

    num *= 100
    num_as_int = int(num)
    
    if num_as_int == num:
        return '%s%%' % num_as_int
    else:
        if num < 10:
            num = '%.02f' % num
        else:
            num = '%.1f' % num
        return '%s%%' % num.rstrip('0').rstrip('.')


def number_as_percentage_change(num):
    if num == 0:
        return '0%'
    else:
        num = ( num * 100 ) - 100
        if num == 0:
            return '0%'
        percentage = '%.2f' % num
        return '%s%%' % percentage.rstrip('0.')


def number_as_grouped_number(num):
    if isinstance(num, basestring):
        num = as_number(num)
        
    if num is None:
        return ''

    num = round(num)
    return locale.format('%d', num, grouping=True)


def string_as_absolute_url(string):
    return join_url_parts(path_prefix, string)


def string_as_asset_url(string):
    return join_url_parts(asset_prefix, string)


def string_as_static_url(string):
    return join_url_parts(static_prefix, digest.digest(string))


def join_url_parts(prefix, suffix):
    return prefix.rstrip('/') + '/' + suffix.lstrip('/')
