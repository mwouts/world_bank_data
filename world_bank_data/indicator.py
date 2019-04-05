import numpy as np
import pandas as pd
from .request import wb_get


def indicators(indicator_list=None, info='value', **params):
    """Return a DataFrame that describes one, multiple or all indicators, indexed by the indicator id.
    :param indicator_list: None (all indicators), the id of an indicator, or a list of multiple ids
    :param info: Chose either 'id' or 'value' for columns 'source' and 'topics'"""

    expected = ['id', 'value']
    if info not in expected:
        raise ValueError("'info' should be one of '{}'".format("', '".join(expected)))

    data = wb_get('indicator', indicator_list, **params)

    # We get a list (indicators) of dictionary (properties)
    columns = data[0].keys()
    df = {}

    for col in columns:
        df[col] = [idx[col][info] if isinstance(idx[col], dict) else idx[col] for idx in data]

    return pd.DataFrame(df, columns=columns).set_index('id')


def indicator(code, country_list=None, labels=True, **params):
    """Return a Series with the indicator data.
    :param code: Indicator code (see indicators())
    :param country_list: None (all countries), the id of a country, or a list of multiple ids
    :param labels: Use labels rather than codes in the index
    :param params: Additional parameters for the World Bank API, like date or mrv"""

    idx = wb_get('country', country_list, 'indicator', code, format='jsonstat', **params)
    idx = idx['WDI']

    dimension = idx.pop('dimension')
    value = idx.pop('value')

    index = pd.MultiIndex.from_product(
        [parse_category(dimension[dim], labels) for dim in dimension['id']],
        names=dimension['id'])

    return pd.Series(value, index=index, name=code)


def parse_category(cat, use_labels):
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
