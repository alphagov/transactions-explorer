from decimal import Decimal
from functools import total_ordering
from itertools import groupby
import re

from lib.filters import as_number
from lib.slugify import keyify, slugify


def latest_quarter(services):
    return max(service.most_recent_kpis['quarter'] for service in services)


def sorted_ignoring_empty_values(services, key, reverse=False):
    services_with_value = [item for item in services if key(item) is not None]
    services_without_value = [item for item in services if key(item) is None]
    return sorted(services_with_value, key=key, reverse=reverse) + services_without_value


class Service:
    valid_quarters = [
        # worked through oldest to newest to calculate %age changes
        '2012_q4',
        '2013_q1',
        '2013_q2',
    ]
    dept_class_table = {
        'AGO': 'single-identity',
        'CO': 'single-identity',
        'BIS': 'bis',
        'DCLG': 'single-identity',
        'DCMS': 'single-identity',
        'DFE': 'single-identity',
        'DEFRA': 'single-identity',
        'DFID': 'single-identity',
        'DFT': 'single-identity',
        'DWP': 'single-identity',
        'DECC': 'single-identity',
        'DH': 'single-identity',
        'FCO': 'single-identity',
        'HMT': 'single-identity',
        'HOME OFFICE': 'ho',
        'MOD': 'mod',
        'MOJ': 'single-identity',
        'NIO': 'single-identity',
        'OAG': 'so',
        'OLHC': 'portcullis',
        'OLHL': 'portcullis',
        'SCOTLAND OFFICE': 'so',
        'UK EXPORT FINANCE': 'single-identity',
        'WO': 'wales',
    }

    def __init__(self, details):
        for key in details:
            setattr( self, keyify(key), details[key] )
        self.has_kpis = False
        self.calculate_quarterly_kpis()
        self.keywords = self._split_keywords(details)

    def calculate_quarterly_kpis(self):
        self.kpis = []
        previous_quarter = None
        self.has_previous_quarter = False
        
        for quarter in self.valid_quarters:
            volume = as_number(self['%s_vol' % quarter])
            if volume is None:
                continue
            
            digital_volume = as_number(self['%s_digital_vol' % quarter])
            if digital_volume == 0:
                takeup = None
            elif digital_volume is not None and volume is not None:
                takeup = digital_volume / volume
            else:
                takeup = None
            
            cost_per = as_number(self['%s_cpt' % quarter])
            
            if cost_per is not None:
                cost = cost_per * volume
            else:
                cost = None
            
            data = {
                'quarter':          Quarter.parse(quarter),
                'takeup':           takeup,
                'cost':             cost,
                'volume':           self['%s_vol' % quarter],
                'volume_num':       volume,
                'digital_volume':   self['%s_digital_vol' % quarter],
                'digital_volume_num': digital_volume,
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
        return re.sub('\s*$', '', self.name_of_service)
    
    @property
    def body(self):
        return self.agency_body
    
    @property
    def description(self):
        return re.sub('\s*$', '', self.description_of_service)

    @property
    def most_recent_kpis(self):
        if len(self.kpis) > 0:
            return self.kpis[-1]

    @property
    def data_coverage(self):
        kpi_provided = lambda kpi: self._attributes_present(kpi,
                                ['digital_volume_num', 'volume_num', 'cost'])

        present = Decimal(len(filter(kpi_provided, self.kpis)))
        total = Decimal(len(self.valid_quarters))

        return present / total

    def _attributes_present(self, kpi, attrs):
        return all(kpi[attr] is not None for attr in attrs)

    def most_recent_kpis_with(self, attrs):
        return next((kpi for kpi in reversed(self.kpis)
                     if self._attributes_present(kpi, attrs)),
                    None)

    @property
    def slug(self):
        return slugify('%s-%s' % (self.abbr, self.name))

    @property
    def link(self):
        return '%s/%s.html' % ('service-details', self.slug)

    @property
    def most_up_to_date_volume(self):
        most_recent_yearly_volume = None
        if self.has_kpis:
            most_recent_yearly_volume = self.most_recent_kpis['volume_num']
        return most_recent_yearly_volume

    def historical_data(self, key):
        data = []
        
        if len(self.kpis) > 1:
            for quarter in reversed(self.kpis):
                data.append({
                    'quarter': quarter['quarter'],
                    'value': quarter.get(key, None),
                })
        
        return data[1:]
    
    @property
    def css_class_postfix(self):
        css_class = self.dept_class_table.get( self.abbr.upper(), None )
        if css_class is not None:
            return css_class
        return None
    
    def __getitem__(self, key):
        return self.__dict__[key]

    def _split_keywords(self, details):
        if not details['Keywords']:
            return []
        return [x.strip() for x in details['Keywords'].split(',')]


@total_ordering
class Quarter:
    def __init__(self, year, quarter):
        self.year = year
        self.quarter = quarter

    def __str__(self):
        return "Q%s %s" % (self.quarter, self.year)

    def __lt__(self, quarter):
        return (self.year, self.quarter) < (quarter.year, quarter.quarter)

    def __eq__(self, quarter):
        return (self.year, self.quarter) == (quarter.year, quarter.quarter)

    @classmethod
    def parse(cls, str):
        m = re.match('(\d\d\d\d)_q(\d)', str)
        return Quarter(int(m.group(1)), int(m.group(2)))


class Department(object):
    @classmethod
    def from_services(cls, services):
        key = lambda s: s.department
        services_by_dept = groupby(sorted(services, key=key), key=key)
        return [Department(name, svcs) for name, svcs in services_by_dept]

    def __init__(self, name, services):
        self.name = name
        self.services = list(services)
        self.aggregator = ServiceKpiAggregator(self.services)

    @property
    def high_volume_count(self):
        return len(filter(lambda s: s.high_volume, self.services))

    @property
    def volume(self):
        return self._aggregate('volume_num')

    @property
    def cost(self):
        return self._aggregate('cost', high_volume_only=True)

    @property
    def abbr(self):
        return self.services[0].abbr

    @property
    def link(self):
        return 'department/%s/by-transactions-per-year/descending.html'\
               % slugify(self.abbr)

    def _aggregate(self, attr, high_volume_only=False):
        return self.aggregator.aggregate([attr], high_volume_only)[0]

    @property
    def takeup(self):
        digital_volume, volume = \
            self.aggregator.aggregate(['digital_volume_num', 'volume_num'],
                                      high_volume_only=True)

        if digital_volume is None:
            return None
        else:
            return digital_volume / volume

    @property
    def data_coverage(self):
        high_volume_services = filter(lambda s: s.high_volume, self.services)
        total_services = len(high_volume_services)

        if total_services == 0:
            return None
        else:
            return sum(service.data_coverage for service in high_volume_services) / total_services


class ServiceKpiAggregator(object):
    def __init__(self, services):
        self.services = services


    def aggregate(self, attrs, high_volume_only=False):
        def included(service):
            return service.most_recent_kpis_with(attrs) is not None and (
                   not high_volume_only or service.high_volume)

        def aggregation(attr):
            values = [service.most_recent_kpis_with(attrs)[attr]
                      for service in self.services
                      if included(service)
                      and service.most_recent_kpis_with(attrs)[attr] is not None]
            if any(values):
                return sum(values)

        return map(aggregation, attrs)


def total_transaction_volume(services):
    def _sum(memo, service):
        number_of_transactions = 0
        if service.has_kpis:
            number_of_transactions = service.most_recent_kpis['volume_num']
        return number_of_transactions + memo

    return reduce(_sum, services, 0)
