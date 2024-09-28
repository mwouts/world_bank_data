"""Get country information"""

import pandas as pd

from .request import wb_get_table
from .search import search


def get_countries(country=None, language=None, id_or_value=None, **params):
    """Return a DataFrame that describes one, multiple or all countries, indexed by the country id.
    :param country: None (all countries), the id of a country, or a list of multiple ids
    :param language: Desired language
    :param id_or_value: Choose either 'id', 'iso2code' or 'value' for columns 'incomeLevel' and 'lendingType'
    """

    table = wb_get_table(
        "country",
        country,
        language=language,
        id_or_value=id_or_value,
        expected=["id", "iso2code", "value"],
        **params
    )

    for col in ["latitude", "longitude"]:
        table[col] = pd.to_numeric(table[col])

    return table


def search_countries(pattern, language=None, **kwargs):
    """Search for the given pattern in the list of countries
    :param pattern: a string or a regular expression
    :param language: Desired language
    :param kwargs: additional arguments for get_countries"""
    return search(get_countries(language=language, **kwargs), pattern)
