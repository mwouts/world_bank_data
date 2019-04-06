from world_bank_data import get_countries
from .tools import assert_numeric_or_string


def test_one_country():
    cnt = get_countries('FRA')
    assert cnt.index == ['FRA']
    assert cnt.lendingType.values[0] == 'Not classified'
    assert cnt.latitude.dtype == float
    assert_numeric_or_string(cnt)


def test_one_country_list():
    cnt = get_countries(['FRA'])
    assert cnt.index == ['FRA']
    assert_numeric_or_string(cnt)


def test_country_language():
    cnt = get_countries(['FRA'], language='fr')
    assert cnt.index == ['FRA']
    assert_numeric_or_string(cnt)
    assert cnt.region[0] == 'Europe et Asie centrale'


def test_two_countries():
    cnt = get_countries(['FRA', 'ITA'])
    assert cnt.index.to_list() == ['FRA', 'ITA']
    assert cnt.latitude.dtype == float
    assert_numeric_or_string(cnt)


def test_all_countries():
    cnt = get_countries()
    assert len(cnt.index) > 200
    assert cnt.latitude.dtype == float
    assert_numeric_or_string(cnt)


def test_one_countries_id():
    cnt = get_countries(['FRA'], id_or_value='id')
    assert cnt.index == ['FRA']
    assert cnt.lendingType.values[0] == 'LNX'
    assert_numeric_or_string(cnt)


def test_one_countries_iso():
    cnt = get_countries(['FRA'], id_or_value='iso2code')
    assert cnt.index == ['FRA']
    assert cnt.lendingType.values[0] == 'XX'
    assert_numeric_or_string(cnt)
