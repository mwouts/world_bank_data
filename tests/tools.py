import pandas as pd


def assert_numeric_or_string(x):
    """Make sure that the Series or Dataframe in argument only contains simple types"""
    if isinstance(x, pd.Series):
        if x.dtype.kind not in ['i', 'f']:
            assert x.apply(type).isin([type(u''), type('')]).all(), \
                "Series '{}' is neither numeric nor strings".format(x.name)
    else:
        for col in x:
            assert_numeric_or_string(x[col])
