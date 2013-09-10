from decimal import Decimal
from functools import total_ordering
from itertools import groupby
import re
import itertools

from lib.filters import as_number
from lib.slugify import keyify, slugify


def latest_quarter(services):
    return max(service.latest_kpi_for('quarter') for service in services if service.has_kpis)


def sorted_ignoring_empty_values(services, key, reverse=False):
    services_with_value = [item for item in services if key(item) is not None]
    services_without_value = [item for item in services if key(item) is None]
    return sorted(services_with_value, key=key, reverse=reverse) + services_without_value


class Service:
    EXPECTED_QUARTERS = [
        # worked through oldest to newest to calculate %age changes
        '2012_q4',
        '2013_q1',
        '2013_q2',
    ]
    COVERAGE_ATTRIBUTES = ['vol', 'digital_vol', 'cpt']

    # A marker used in the spreadsheet to show that a metric was not requested
    NOT_REQUESTED_MARKER = '***'

    def __init__(self, details):
        for key in details:
            setattr(self, keyify(key), details[key])
        self.has_kpis = False
        self.calculate_quarterly_kpis()
        self.keywords = self._split_keywords(details)

    def calculate_quarterly_kpis(self):
        self.kpis = []
        previous_quarter = None
        self.has_previous_quarter = False

        for quarter in self.EXPECTED_QUARTERS:
            volume = as_number(self['%s_vol' % quarter])
            if volume is None:
                continue

            digital_volume = as_number(self['%s_digital_vol' % quarter])
            if digital_volume == 0:
                takeup = 0
            elif digital_volume is not None and volume is not None:
                takeup = digital_volume / volume
            else:
                takeup = None

            cost_per_transaction = as_number(self['%s_cpt' % quarter])

            if cost_per_transaction is not None:
                cost = cost_per_transaction * volume
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
                'cost_per_number':  cost_per_transaction,
                'cost_per_digital': self['%s_digital_cpt' % quarter],
                'completion':       self['%s_completion_rate' % quarter],
                'satisfaction':     self['%s_user_satisfaction' % quarter],
            }

            def change_factor(previous, current):
                factor = None
                if current is not None and previous is not None and previous != 0:
                    factor = current / previous
                return factor

            if previous_quarter is not None:
                self.has_previous_quarter = True
                data['volume_change'] = change_factor(previous_quarter['volume_num'], volume)
                data['takeup_change'] = change_factor(previous_quarter['takeup'], takeup)
                data['cost_per_change'] = change_factor(previous_quarter['cost_per_number'], cost_per_transaction)
                data['cost_change'] = change_factor(previous_quarter['cost'], cost)
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
    def agency_abbreviation(self):
        if self.agency_abbr is None or len(self.agency_abbr) == 0:
            return self.body
        else:
            return self.agency_abbr

    @property
    def description(self):
        return re.sub('\s*$', '', self.description_of_service)

    def latest_kpi_for(self, attribute):
        latest_kpis = self._most_recent_kpis
        if latest_kpis is None:
            return None
        else:
            return latest_kpis.get(attribute)

    @property
    def _most_recent_kpis(self):
        if len(self.kpis) > 0:
            return self.kpis[-1]

    @property
    def data_coverage(self):
        def is_requested(attr):
            return str(self[attr]).lower() != self.NOT_REQUESTED_MARKER

        def is_provided(attr):
            return as_number(self[attr]) is not None

        all_attrs = map('_'.join, itertools.product(
            self.EXPECTED_QUARTERS, self.COVERAGE_ATTRIBUTES))
        all_requested = filter(is_requested, all_attrs)
        all_provided = filter(is_provided, all_requested)

        return Coverage(len(all_provided), len(all_requested))

    def _attributes_present(self, kpi, attrs):
        return all(kpi[attr] is not None for attr in attrs)

    def find_recent_kpis_with_attributes(self, attrs):
        return next((kpi for kpi in reversed(self.kpis)
                     if self._attributes_present(kpi, attrs)),
                    None)

    @property
    def slug(self):
        return slugify('%s-%s' % (self.abbr, self.name))

    @property
    def link(self):
        return '%s/%s' % ('service-details', self.slug)

    @property
    def has_details_page(self):
        return self.detailed_view == 'yes'

    @property
    def most_up_to_date_volume(self):
        most_recent_yearly_volume = None
        if self.has_kpis:
            most_recent_yearly_volume = self.latest_kpi_for('volume_num')
        return most_recent_yearly_volume

    def historical_data_before(self, quarter, key):
        key_data = lambda k: {'quarter': k['quarter'], 'value': k.get(key)}
        previous_kpis = filter(lambda k: k['quarter'] < quarter, self.kpis)

        return map(key_data, reversed(previous_kpis))

    def __getitem__(self, key):
        return getattr(self, key)

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

    def __repr__(self):
        return '<Quarter year=%s quarter=%s>' % (self.year, self.quarter)

    @classmethod
    def parse(cls, str):
        m = re.match('(\d\d\d\d)_q(\d)', str)
        return Quarter(int(m.group(1)), int(m.group(2)))


class Department(object):
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
        'HMRC': 'hmrc',
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
    def name_slug(self):
        return slugify(self.name)

    @property
    def css_class_postfix(self):
        css_class = self.dept_class_table.get(self.abbr.upper(), None)
        if css_class is not None:
            return css_class
        return None

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
        return 'department/%s/by-transactions-per-year/descending'\
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
            return sum(service.data_coverage.percentage for service in high_volume_services) / total_services


class ServiceKpiAggregator(object):
    def __init__(self, services):
        self.services = services

    def aggregate(self, attrs, high_volume_only=False):
        def included(service):
            return service.find_recent_kpis_with_attributes(attrs) is not None and (
                   not high_volume_only or service.high_volume)

        def aggregation(attr):
            values = [service.find_recent_kpis_with_attributes(attrs)[attr]
                      for service in self.services
                      if included(service)
                      and service.find_recent_kpis_with_attributes(attrs)[attr] is not None]
            if any(values):
                return sum(values)

        return map(aggregation, attrs)


def total_transaction_volume(services):
    def _sum(memo, service):
        number_of_transactions = 0
        if service.has_kpis:
            number_of_transactions = service.latest_kpi_for('volume_num')
        return number_of_transactions + memo

    return reduce(_sum, services, 0)


class Coverage(object):
    def __init__(self, provided, requested):
        self.provided = provided
        self.requested = requested

    @property
    def percentage(self):
        return Decimal(self.provided) / Decimal(self.requested)