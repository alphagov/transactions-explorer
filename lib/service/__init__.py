import re


def keyify(text):
    unclean = re.sub( r'\W+', '_', text.lower() )
    more_clean = re.sub( r'_$', '', unclean )
    return re.sub( r'^_', '', more_clean )


class Service:
    valid_quarters = [
        # worked through oldest to newest to calculate %age changes
        '2012_q4',
        '2013_q1',
        '2013_q2',
    ]
    
    def __init__(self, details):
        for key in details:
            setattr( self, keyify(key), details[key] )
    
    @property
    def name(self):
        return self.name_of_service
