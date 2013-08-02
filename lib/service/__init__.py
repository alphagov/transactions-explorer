import re

from lib.filters import as_number, period_as_text
from lib.slugify import keyify


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
        self.has_kpis = False
        self.calculate_quarterly_kpis()
    
    def calculate_quarterly_kpis(self):
        self.kpis = []
        previous_quarter = None
        self.has_previous_quarter = False
        
        for quarter in self.valid_quarters:
            volume = as_number(self['%s_vol' % quarter])
            if volume is None:
                continue
            
            digital_volume = as_number(self['%s_digital_vol' % quarter])
            if digital_volume is not None and volume is not None:
                takeup = digital_volume / volume
            else:
                takeup = None
            
            cost_per = as_number(self['%s_cpt' % quarter])
            
            if cost_per is not None:
                cost = cost_per * volume
            else:
                cost = None
            
            data = {
                'quarter':          period_as_text(quarter),
                'takeup':           takeup,
                'cost':             cost,
                'volume':           self['%s_vol' % quarter],
                'volume_num':       volume,
                'digital_volume':   self['%s_digital_vol' % quarter],
                'cost_per':         self['%s_cpt' % quarter],
                'cost_per_number':  cost_per,
                'cost_per_digital': self['%s_digital_cpt' % quarter],
                'completion':       self['%s_completion_rate' % quarter],
                'satisfaction':     self['%s_user_satisfaction' % quarter],
            }
            
            if previous_quarter is not None:
                self.has_previous_quarter = True
                if previous_quarter['volume_num'] is not None:
                    if previous_quarter['volume_num'] == 0:
                        data['volume_change'] = volume * 100
                    else:
                        data['volume_change'] = volume / previous_quarter['volume_num']
                else:
                    data['volume_change'] = None
                if takeup is not None and previous_quarter['takeup'] is not None:
                    if previous_quarter['takeup'] == 0:
                        data['takeup_change'] = takeup * 100
                    else:
                        data['takeup_change'] = takeup / previous_quarter['takeup']
                else:
                    data['takeup_change'] = None
                if cost and previous_quarter['cost']:
                    if previous_quarter['cost'] == 0:
                        data['cost_change'] = cost * 100
                    else:
                        data['cost_change'] = cost / previous_quarter['cost']
                else:
                    data['cost_change'] = None
                if cost_per and previous_quarter['cost_per_number']:
                    if previous_quarter['cost_per_number'] == 0:
                        data['cost_per_change'] = cost_per * 100
                    else:
                        data['cost_per_change'] = cost_per / previous_quarter['cost_per_number']
                else:
                    data['cost_per_change'] = None
                data['previous_quarter'] = previous_quarter['quarter']
            
            previous_quarter = data
            self.kpis.append(data)
            self.has_kpis = True
    
    @property
    def name(self):
        return self.name_of_service
    
    def __getitem__(self, key):
        return self.__dict__[key]
    
