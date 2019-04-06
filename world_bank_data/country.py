"""Get country information"""

import pandas as pd
from .request import wb_get, extract_preferred_field
from .options import default_field, default_language


def get_countries(country=None, language=default_language, field=default_field, **params):
    """Return a DataFrame that describes one, multiple or all countries, indexed by the country id.
    :param country: None (all countries), the id of a country, or a list of multiple ids
    :param language: Desired language
    :param field: Chose either 'id', 'iso2code' or 'value' for columns 'incomeLevel' and 'lendingType'"""

    expected = ['id', 'iso2code', 'value']
    if field not in expected:
        raise ValueError("'field' should be one of '{}'".format("', '".join(expected)))

    data = wb_get('country', country, language=language, **params)

    # We get a list (countries) of dictionary (properties)
    columns = data[0].keys()
    table = {}

    for col in columns:
        table[col] = [extract_preferred_field(cnt[col], field) for cnt in data]

    table = pd.DataFrame(table, columns=columns).set_index('id')

    for col in ['latitude', 'longitude']:
        table[col] = pd.to_numeric(table[col])

    return table
