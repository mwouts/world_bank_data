"""Get country information"""

import pandas as pd
from .request import wb_get_table
from .search import search


def get_countries(country=None, language=None, field=None, **params):
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


def search_countries(pattern, language=None):
    """Search for the given pattern in the list of countries
    :param pattern: a string or a regular expression
    :param language: Desired language"""
    return search(get_countries(language=language), pattern)
