from world_bank_data import indicators, indicator


def test_indicators_one():
    idx = indicators('SP.POP.TOTL')
    assert idx.index == ['SP.POP.TOTL']


def test_indicators():
    idx = indicators()
    assert len(idx.index) > 1000


def test_indicator_most_recent_value():
    idx = indicator('SP.POP.TOTL', mrv=1)
    assert len(idx.index) > 200

    idx_mrv5 = indicator('SP.POP.TOTL', mrv=5)
    assert len(idx_mrv5.index) == 5 * len(idx.index)
