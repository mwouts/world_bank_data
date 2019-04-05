from world_bank_data import regions
from .tools import assert_numeric_or_string


def test_one_region():
    reg = regions('AFR')
    assert 'id' not in reg.columns
    assert reg.index == ['AFR']
    assert_numeric_or_string(reg)


def test_one_region_list():
    reg = regions(['AFR'])
    assert 'id' not in reg.columns
    assert reg.index == ['AFR']
    assert_numeric_or_string(reg)


def test_two_regions():
    reg = regions(['AFR', 'ANR'])
    assert 'id' not in reg.columns
    assert reg.index.to_list() == ['AFR', 'ANR']
    assert_numeric_or_string(reg)


def test_all_regions():
    reg = regions()
    assert 'id' not in reg.columns
    assert len(reg.index) > 30
    assert_numeric_or_string(reg)
