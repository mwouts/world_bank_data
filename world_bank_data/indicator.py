"""Get indicators and their values"""

import numpy as np
import pandas as pd

import world_bank_data.options as options

from .request import wb_get, wb_get_table
from .search import search


def get_indicators(indicator=None, language=None, id_or_value=None, **params):
    """Return a DataFrame that describes one, multiple or all indicators, indexed by the indicator id.
    :param indicator: None (all indicators), the id of an indicator, or a list of multiple ids
    :param language: Desired language
    :param id_or_value: Choose either 'id' or 'value' for columns 'source' and 'topics'
    """

    if id_or_value == "iso2code":
        id_or_value = "id"

    return wb_get_table(
        "indicator",
        indicator,
        language=language,
        id_or_value=id_or_value,
        expected=["id", "value"],
        **params
    )


def search_indicators(pattern, language=None, **kwargs):
    """Search the indicators that match the given pattern
    :param pattern: a string or a regular expression
    :param language: the desired language
    :param kwargs: additional arguments for get_indicators"""
    return search(get_indicators(language=language, **kwargs), pattern)


def get_series(
    indicator, country=None, id_or_value=None, simplify_index=False, **params
):
    """Return a Series with the indicator data.
    :param indicator: Indicator code (see indicators())
    :param country: None (all countries), the id of a country, or a list of multiple country codes
    :param id_or_value: Should the index have codes or labels?
    :param simplify_index: Drop index levels that have a single value
    :param params: Additional parameters for the World Bank API, like date or mrv"""

    id_or_value = id_or_value or options.id_or_value
    params["format"] = "jsonstat"

    idx = wb_get("country", country, "indicator", indicator, **params)
    _, idx = idx.popitem()

    dimension = idx.pop("dimension")
    value = idx.pop("value")

    index = [
        _parse_category(dimension[dim], id_or_value == "value")
        for dim in dimension["id"]
    ]
    if not id_or_value:
        for idx, name in zip(index, dimension["id"]):
            idx.name = name

    if simplify_index:
        index = [dim for dim in index if len(dim) != 1]

    if len(index) > 1:
        # Our series is indexed by a multi-index
        index = pd.MultiIndex.from_product(index, names=[dim.name for dim in index])
    elif len(index) == 1:
        # A simple index is enough
        index = index[0]
    else:
        # Index has dimension zero. Data should be a scalar
        assert len(value) == 1, "Data has no dimension and was expected to be a scalar"
        return value[0]

    return pd.Series(value, index=index, name=indicator)


def _parse_category(cat, use_labels):
    name = cat["label"]
    cat = cat["category"]

    index = np.array(list(cat["index"].values()))
    codes = np.array(list(cat["index"].keys()))

    codes = pd.Series(codes, index=index, name=name).sort_index()
    if not use_labels:
        return codes

    codes2 = np.array(list(cat["label"].keys()))
    labels = np.array(list(cat["label"].values()))
    labels = pd.Series(labels, index=codes2, name=name).sort_index()

    return pd.Series(labels.loc[codes].values, index=codes.index, name=name)
