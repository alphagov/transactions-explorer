import re

def slugify(text):
    slug = re.sub( r'\W+', '-', text.lower() )
    slug = slug.replace('-and-', '-')
    return slug

def keyify(text):
    unclean = re.sub( r'\W+', '_', text.lower() )
    more_clean = re.sub( r'_$', '', unclean )
    return re.sub( r'^_', '', more_clean )
