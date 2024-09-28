"""Search in a table"""

import re

import pandas as pd


def search(table, pattern, columns=None):
    """Return the rows of the table for which a column matches the pattern"""
    assert isinstance(table, pd.DataFrame), "'table' must be a Pandas DataFrame"

    if columns is None:
        columns = [col for col in table.columns if table[col].dtype.kind == "O"]

    if not columns:
        raise ValueError(
            "Please specific a non-empty columns arguments, and run the search "
            "on a table that has string columns"
        )

    if isinstance(pattern, str):
        if not pattern.startswith(".*"):
            pattern = ".*(" + pattern + ")"
        pattern = re.compile(pattern, re.IGNORECASE)

    found = pd.Series(0, index=table.index)
    for col in columns:
        found += table[col].apply(lambda x: 1 if pattern.match(x) else 0)

    return table.loc[found > 0]
