import pandas as pd
from .request import wb_get


def income_levels(ids=None, **params):
    """Return a DataFrame that describes one, multiple or all income levels, indexed by the IL id.
    :param ids: None (all income levels), the id of a income level, or a list of multiple ids"""

    data = wb_get('incomelevel', ids, **params)

    columns = data[0].keys()
    df = {}

    for col in columns:
        df[col] = [cnt[col] for cnt in data]

    return pd.DataFrame(df, columns=columns).set_index('id')


def lending_types(ids=None, **params):
    """Return a DataFrame that describes one, multiple or all lending types, indexed by the LT id.
    :param ids: None (all lending types), the id of a lending type, or a list of multiple ids"""

    data = wb_get('lendingtypes', ids, **params)

    columns = data[0].keys()
    df = {}

    for col in columns:
        df[col] = [cnt[col] for cnt in data]

    return pd.DataFrame(df, columns=columns).set_index('id')
