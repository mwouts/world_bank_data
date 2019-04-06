import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
from world_bank_data import search


@pytest.fixture()
def table():
    return pd.DataFrame({'number': [1, 2, 3],
                         'short': ['a', 'b', 'c'],
                         'letter': ['Alpha', 'Beta', 'Gamma']})


def test_search(table):
    assert_frame_equal(table, search(table, 'a'))
    assert_frame_equal(table.iloc[[1]], search(table, 'b'))
    assert_frame_equal(table.iloc[[1]], search(table, 'eta'))
    assert_frame_equal(table.iloc[[0, 2]], search(table, 'ma|ha'))
