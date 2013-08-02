import locale

from re import match, sub
from math import ceil

locale.setlocale(locale.LC_ALL, 'en_GB')


def as_number(num):
    if num:
        just_numbers = sub( r'[^\d\.]+', '', num)
        try:
            return float(just_numbers)
        except ValueError:
            pass
    return None


def number_as_magnitude(num):
    if num is None:
        return 0
    if type(num) is str or type(num) is unicode:
        num = as_number(num)
    
    if num < 10:
        return '%.2f' % num
    elif num < 100:
        return '%.1f' % num
    elif num < 1000:
        return int(ceil(num))
    elif num < 10000:
        return '%.2fk' % (num / 1000)
    elif num < 100000:
        return '%.1fk' % (num / 1000)
    elif num < 1000000:
        return '%dk' % round(num / 1000)
    elif num < 10000000:
        return '%.2fm' % (num / 1000000)
    elif num < 100000000:
        return '%.1fm' % (num / 1000000)
    elif num < 1000000000:
        return '%dm' % round(num / 1000000)
    elif num < 10000000000:
        return '%.2fbn' % (num / 1000000000)
    elif num < 100000000000:
        return '%.1fbn' % (num / 1000000000)
    return '%dbn' % round(num / 1000000000)


def number_as_financial_magnitude(num):
    if num is None:
        return 0
    if type(num) is str or type(num) is unicode:
        num = as_number(num)
    
    if num < 100:
        return '%.2f' % num
    elif num < 1000:
        return int(ceil(num))
    elif num < 10000:
        return '%.2fk' % (num / 1000)
    elif num < 100000:
        return '%.1fk' % (num / 1000)
    elif num < 1000000:
        return '%dk' % (num / 1000)
    elif num < 10000000:
        return '%.2fm' % (num / 1000000)
    elif num < 100000000:
        return '%.1fm' % (num / 1000000)
    elif num < 1000000000:
        return '%dm' % (num / 1000000)
    elif num < 10000000000:
        return '%.2fbn' % (num / 1000000000)
    elif num < 100000000000:
        return '%.1fbn' % (num / 1000000000)
    return '%dbn' % (num / 1000000000)


def number_as_percentage(num):
    if type(num) is str or type(num) is unicode:
        num = as_number(num)

    if num == None:
        return ''
    
    num = num * 100
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
    if type(num) is str or type(num) is unicode:
        num = float(as_number(num))
    
    if num < 100:
        num = '%.02f' % num
        return num
        return num.rstrip('0.')
    else:
        num = round(num)
        return locale.format('%d', num, grouping=True)


def period_as_text(str):
    m = match('(\d\d\d\d)_q(\d)', str)
    return 'Q%s %s' % ( m.group(2), m.group(1) )
