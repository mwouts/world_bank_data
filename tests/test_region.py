import pytest

from world_bank_data import get_regions
from .tools import assert_numeric_or_string


def test_one_region():
    reg = get_regions('AFR')
    assert 'id' not in reg.columns
    assert reg.index == ['AFR']
    assert_numeric_or_string(reg)


def test_region_language():
    reg = get_regions(['ECS'], language='fr')
    assert reg.name[0] == 'Europe et Asie centrale'


def test_one_region_list():
    reg = get_regions(['AFR'])
    assert 'id' not in reg.columns
    assert reg.index == ['AFR']
    assert_numeric_or_string(reg)


@pytest.mark.xfail(reason="The provided parameter value is not valid")
def test_two_regions():
    reg = get_regions(['AFR', 'ANR'])
    assert 'id' not in reg.columns
    assert set(reg.index) == set(['AFR', 'ANR'])
    assert_numeric_or_string(reg)


def test_all_regions():
    reg = get_regions()
    assert 'id' not in reg.columns
    assert len(reg.index) > 30
    assert_numeric_or_string(reg)
