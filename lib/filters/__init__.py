from re import match, sub


def as_number(num):
    if num:
        just_numbers = sub( r'[^\d\.]+', '', num)
        try:
            return float(just_numbers)
        except ValueError:
            pass
    return None


def period_as_text(str):
    m = match('(\d\d\d\d)_q(\d)', str)
    return 'Q%s %s' % ( m.group(2), m.group(1) )
