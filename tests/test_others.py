from world_bank_data import lending_types, income_levels


def test_lending_types():
    df = lending_types()
    assert df.index.names == ['id']
    assert df.columns.to_list() == ['iso2code', 'value']


def test_income_levels():
    df = income_levels()
    assert df.index.names == ['id']
    assert df.columns.to_list() == ['iso2code', 'value']
