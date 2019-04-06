"""Get indicators and their values"""

import numpy as np
import pandas as pd
from .request import wb_get, wb_get_table
from .options import default_field, default_language


def get_indicators(indicator=None, language=default_language, field=default_field, **params):
    """Return a DataFrame that describes one, multiple or all indicators, indexed by the indicator id.
    :param indicator: None (all indicators), the id of an indicator, or a list of multiple ids
    :param language: Desired language
    :param field: Chose either 'id' or 'value' for columns 'source' and 'topics'"""

    if field == 'iso2code':
        field = 'id'

    return wb_get_table('indicator', indicator, language=language, field=field, expected=['id', 'value'], **params)


def get_series(indicator, country_list=None, field='value', drop_constant_index=False, **params):
    """Return a Series with the indicator data.
    :param indicator: Indicator code (see indicators())
    :param country_list: None (all countries), the id of a country, or a list of multiple ids
    :param field: Choose between 'value' and 'id' for the index
    :param drop_constant_index: Drop indexes when they take a single value
    :param params: Additional parameters for the World Bank API, like date or mrv"""

    idx = wb_get('country', country_list, 'indicator', indicator, data_format='jsonstat', **params)
    idx = idx['WDI']

    dimension = idx.pop('dimension')
    value = idx.pop('value')

    index = [_parse_category(dimension[dim], field == 'value') for dim in dimension['id']]
    if field != 'value':
        for idx, name in zip(index, dimension['id']):
            idx.name = name

    if drop_constant_index:
        index = [dim for dim in index if len(dim) != 1]

    return pd.Series(value, index=pd.MultiIndex.from_product(index, names=[dim.name for dim in index]), name=indicator)


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
