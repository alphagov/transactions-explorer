from re import sub


def slugify(text):
    slug = sub( r'\W+', '-', text.lower() )
    slug = slug.replace('-and-', '-')
    return slug

def keyify(text):
    unclean = sub( r'\W+', '_', text.lower() )
    more_clean = sub( r'_$', '', unclean )
    return sub( r'^_', '', more_clean )
