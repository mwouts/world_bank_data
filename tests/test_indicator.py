import pytest
from world_bank_data import get_indicators, get_series
from .tools import assert_numeric_or_string


def test_indicators_one():
    idx = get_indicators('SP.POP.TOTL')
    assert idx.index == ['SP.POP.TOTL']
    assert_numeric_or_string(idx)


def test_indicators_two():
    with pytest.raises(RuntimeError):
        get_indicators(['SP.POP.0014.TO.ZS', 'SP.POP.TOTL'])


def test_indicators():
    idx = get_indicators()
    assert len(idx.index) > 1000
    assert_numeric_or_string(idx)


def test_indicator_most_recent_value():
    idx = get_series('SP.POP.TOTL', mrv=1)
    assert len(idx.index) > 200
    assert_numeric_or_string(idx)

    idx_mrv5 = get_series('SP.POP.TOTL', mrv=5)
    assert len(idx_mrv5.index) == 5 * len(idx.index)
    assert_numeric_or_string(idx_mrv5)
