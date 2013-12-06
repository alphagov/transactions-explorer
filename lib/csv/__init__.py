#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lib.filters import as_number
from lib.service import latest_quarter

CSV_FORMAT = [("Department", lambda s: s.department),
              ("Department Abbreviation", lambda s: s.abbr),
              ("Body/Agency", lambda s: s.body),
              ("Agency Abbreviation", lambda s: s.agency_abbr),
              ("Name of service", lambda s: s.name),
              ("April 2011 to March 2012: volume",
               lambda s: as_number(getattr(s, "2012_q4_vol"))),
              ("April 2011 to March 2012: digital volume",
               lambda s: as_number(getattr(s, "2012_q4_digital_vol"))),
              ("April 2011 to March 2012: cost per transaction (£)",
               lambda s: as_number(getattr(s, "2012_q4_cpt"))),
              ("January 2012 to December 2012: volume",
               lambda s: as_number(getattr(s, "2013_q1_vol"))),
              ("January 2012 to December 2012: digital volume",
               lambda s: as_number(getattr(s, "2013_q1_digital_vol"))),
              ("January 2012 to December 2012: cost per transaction (£)",
               lambda s: as_number(getattr(s, "2013_q1_cpt"))),
              ("April 2012 to March 2013: volume",
               lambda s: as_number(getattr(s, "2013_q2_vol"))),
              ("April 2012 to March 2013: digital volume",
               lambda s: as_number(getattr(s, "2013_q2_digital_vol"))),
              ("April 2012 to March 2013: cost per transaction (£)",
               lambda s: as_number(getattr(s, "2013_q2_cpt"))),
              ("July 2012 to June 2013: volume",
               lambda s: as_number(getattr(s, "2013_q3_vol"))),
              ("July 2012 to June 2013: digital volume",
               lambda s: as_number(getattr(s, "2013_q3_digital_vol"))),
              ("July 2012 to June 2013: cost per transaction (£)",
               lambda s: as_number(getattr(s, "2013_q3_cpt"))),
              ("Latest volume", 
                lambda s: as_number(s.latest_kpi_for('volume'))),
              ("Latest digital volume",
                lambda s: as_number(s.latest_kpi_for('digital_volume'))),
              ("Latest cost per transaction (£)",
                lambda s: as_number(s.latest_kpi_for('cost_per'))),
              ("Service Type", lambda s: s.category),
              ("URL", lambda s: s.url),
              ("Description of service", lambda s: s.description),
              ("Notes on costs", lambda s: s.notes_on_costs),
              ("Other notes", lambda s: s.other_notes),
              ("Customer type", lambda s: s.customer_type),
              ("Business model", lambda s: s.business_model)]


JSON_SEARCH_FORMAT = [("department", lambda s: s.department),
                      ("departmentAbbreviation", lambda s: s.abbr),
                      ("agencyOrBody", lambda s: s.body),
                      ("agencyOrBodyAbbreviation", lambda s: s.agency_abbr),
                      ("service", lambda s: s.name),
                      ("keywords", lambda s: s.keywords),
                      ("transactionsPerYear",
                       lambda s: s.most_up_to_date_volume),
                      ("transactionLink", lambda s: s.url),
                      ("detailsLink",
                       lambda s: s.link if s.has_details_page else ""),
                      ("category", lambda s: s.category)]


def encode(value):
    if isinstance(value, basestring):
        return value.encode('utf8')
    else:
        return value


def tabular_map(mappings, services):
    column_name = lambda m: m[0]

    def apply_mappings(service):
        return [encode(fn(service)) for _, fn in mappings]

    columns = map(column_name, mappings)

    return [columns] + map(apply_mappings, services)


def dict_map(mappings, services):
    key = lambda m: m[0]
    val = lambda m, s: m[1](s)
    dicts = []

    latest = latest_quarter(services)
   
    for service in services:
      key_vals = []
      for mapping in mappings:
        key_vals.append([key(mapping), val(mapping, service)])

      # Test and append quarter as string IF it's historical data
      quarter = service.latest_kpi_for('quarter')
      if quarter is not None and quarter < latest:
          key_vals.append(["historic", str(quarter)])

      dicts.append(dict(key_vals))

    return dicts


def map_services_to_csv_data(services):
    return tabular_map(
        CSV_FORMAT,
        services
    )


def map_services_to_dicts(services):
    return dict_map(
        JSON_SEARCH_FORMAT,
        services
    )
