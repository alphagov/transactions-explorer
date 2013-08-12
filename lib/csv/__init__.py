from lib.filters import as_number

CSV_FORMAT = [("Department", lambda s: s.department),
              ("Department Abbreviation", lambda s: s.abbr),
              ("Body/Agency", lambda s: s.body),
              ("Agency Abbreviation", lambda s: s.agency_abbr),
              ("Name of service", lambda s: s.name),
              ("2012 Q4: volume",
               lambda s: as_number(getattr(s, "2012_q4_vol"))),
              ("2012 Q4: digital volume",
               lambda s: as_number(getattr(s, "2012_q4_digital_vol"))),
              ("2012 Q4: cost per transaction",
               lambda s: as_number(getattr(s, "2012_q4_cpt"))),
              ("2013 Q1: volume",
               lambda s: as_number(getattr(s, "2013_q1_vol"))),
              ("2013 Q1: digital volume",
               lambda s: as_number(getattr(s, "2013_q1_digital_vol"))),
              ("2013 Q1: cost per transaction",
               lambda s: as_number(getattr(s, "2013_q1_cpt"))),
              ("2013 Q2: volume",
               lambda s: as_number(getattr(s, "2013_q2_vol"))),
              ("2013 Q2: digital volume",
               lambda s: as_number(getattr(s, "2013_q2_digital_vol"))),
              ("2013 Q2: cost per transaction",
               lambda s: as_number(getattr(s, "2013_q2_cpt"))),
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
                       lambda s: s.most_up_to_date_volume)]


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

    for service in services:
        key_vals = []
        for mapping in mappings:
            key_vals.append([key(mapping), val(mapping, service)])
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
