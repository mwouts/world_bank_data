import pandas as pd
from .request import wb_get, collapse


def countries(country_list=None, info='value', **params):
    """Return a DataFrame that describes one, multiple or all countries, indexed by the country id.
    :param country_list: None (all countries), the id of a country, or a list of multiple ids
    :param info: Chose either 'id', 'iso2code' or 'value' for columns 'incomeLevel' and 'lendingType'"""

    expected = ['id', 'iso2code', 'value']
    if info not in expected:
        raise ValueError("'info' should be one of '{}'".format("', '".join(expected)))

    country_data = wb_get('country', country_list, **params)

    # We get a list (countries) of dictionary (properties)
    columns = country_data[0].keys()
    df = {}

    for col in columns:
        df[col] = [cnt[col][info] if isinstance(cnt[col], dict) else cnt[col] for cnt in country_data]

    df = pd.DataFrame(df, columns=columns).set_index('id')

    for col in ['latitude', 'longitude']:
        df[col] = pd.to_numeric(df[col])

    return df
