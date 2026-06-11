import pandas as pd


def assert_numeric_or_string(x):
    """Make sure that the Series or Dataframe in argument only contains simple types"""
    if isinstance(x, pd.Series):
        if x.dtype.kind not in ["i", "f"]:
            assert x.apply(type).isin([str, str]).all(), (
                f"Series '{x.name}' is neither numeric nor strings"
            )
    else:
        for col in x:
            assert_numeric_or_string(x[col])
