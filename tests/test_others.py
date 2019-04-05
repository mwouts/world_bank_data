from world_bank_data import lending_types, income_levels
from .tools import assert_numeric_or_string


def test_lending_types():
    df = lending_types()
    assert df.index.names == ['id']
    assert df.columns.to_list() == ['iso2code', 'value']
    assert_numeric_or_string(df)


def test_income_levels():
    df = income_levels()
    assert df.index.names == ['id']
    assert df.columns.to_list() == ['iso2code', 'value']
    assert_numeric_or_string(df)
