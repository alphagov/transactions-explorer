from re import sub


def slugify(text):
    text = text.lower()
    text = text.replace('\'', '')
    slug = sub( r'\W+', '-', text )
    slug = slug.replace('-and-', '-')
    return slug.strip('-')

def keyify(text):
    unclean = sub( r'\W+', '_', text.lower() )
    more_clean = sub( r'_$', '', unclean )
    return sub( r'^_', '', more_clean )
