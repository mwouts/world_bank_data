"""Get indicators and their values"""

import numpy as np
import pandas as pd
from .request import wb_get, extract_preferred_field
from .options import default_field, default_language


def get_indicators(indicator=None, language=default_language, field=default_field, **params):
    """Return a DataFrame that describes one, multiple or all indicators, indexed by the indicator id.
    :param indicator: None (all indicators), the id of an indicator, or a list of multiple ids
    :param language: Desired language
    :param field: Chose either 'id' or 'value' for columns 'source' and 'topics'"""

    if field == 'iso2code':
        field = 'id'

    expected = ['id', 'value']
    if field not in expected:
        raise ValueError("'field' should be one of '{}'".format("', '".join(expected)))

    data = wb_get('indicator', indicator, language=language, **params)
    if not data:
        raise RuntimeError('The request returned no data')

    # We get a list (indicators) of dictionary (properties)
    columns = data[0].keys()
    table = {}

    for col in columns:
        table[col] = [extract_preferred_field(idx[col], field) for idx in data]

    return pd.DataFrame(table, columns=columns).set_index('id')


def get_series(indicator, country_list=None, labels=True, **params):
    """Return a Series with the indicator data.
    :param indicator: Indicator code (see indicators())
    :param country_list: None (all countries), the id of a country, or a list of multiple ids
    :param labels: Use labels rather than codes in the index
    :param params: Additional parameters for the World Bank API, like date or mrv"""

    idx = wb_get('country', country_list, 'indicator', indicator, data_format='jsonstat', **params)
    idx = idx['WDI']

    dimension = idx.pop('dimension')
    value = idx.pop('value')

    index = pd.MultiIndex.from_product(
        [_parse_category(dimension[dim], labels) for dim in dimension['id']],
        names=dimension['id'])

    return pd.Series(value, index=index, name=indicator)


def _parse_category(cat, use_labels):
    name = cat['label']
    cat = cat['category']

    index = np.array(list(cat['index'].values()))
    assert np.array_equal(index, np.arange(len(index))), 'Index should be ordered. Please use Python 3.6 or above.'

    codes = np.array(list(cat['index'].keys()))
    if not use_labels:
        return pd.Series(codes, index=index, name=name)

    codes2 = np.array(list(cat['label'].keys()))
    assert np.array_equal(codes, codes2), 'Codes should be identical'

    labels = np.array(list(cat['label'].values()))
    return pd.Series(labels, index=index, name=name)
