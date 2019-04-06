"""Get country information"""

import pandas as pd
from .request import wb_get_table
from .options import default_field, default_language


def get_countries(country=None, language=default_language, field=default_field, **params):
    """Return a DataFrame that describes one, multiple or all countries, indexed by the country id.
    :param country: None (all countries), the id of a country, or a list of multiple ids
    :param language: Desired language
    :param field: Chose either 'id', 'iso2code' or 'value' for columns 'incomeLevel' and 'lendingType'"""

    table = wb_get_table('country', country, language=language,
                         field=field, expected=['id', 'iso2code', 'value'],
                         **params)

    for col in ['latitude', 'longitude']:
        table[col] = pd.to_numeric(table[col])

    return table
