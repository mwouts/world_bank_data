import pandas as pd


def assert_numeric_or_string(x):
    """Make sure that the Series or Dataframe in argument only contains simple types"""
    if isinstance(x, pd.Series):
        if x.dtype.kind not in ['i', 'f']:
            for y in x:
                assert isinstance(y, str), 'Series {} is expected to contain ' \
                                           'only numeric or string types, found {}'.format(x.name, y)
    else:
        for col in x:
            assert_numeric_or_string(x[col])
