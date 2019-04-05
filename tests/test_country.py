from world_bank_data import countries


def test_one_country():
    cnt = countries('FRA')
    assert cnt.index == ['FRA']
    assert cnt.lendingType.values[0] == 'Not classified'
    assert cnt.latitude.dtype == float


def test_one_country_list():
    cnt = countries(['FRA'])
    assert cnt.index == ['FRA']


def test_two_countries():
    cnt = countries(['FRA', 'ITA'])
    assert cnt.index.to_list() == ['FRA', 'ITA']
    assert cnt.latitude.dtype == float


def test_all_countries():
    cnt = countries()
    assert len(cnt.index) > 200
    assert cnt.latitude.dtype == float


def test_one_countries_id():
    cnt = countries(['FRA'], info='id')
    assert cnt.index == ['FRA']
    assert cnt.lendingType.values[0] == 'LNX'


def test_one_countries_iso():
    cnt = countries(['FRA'], info='iso2code')
    assert cnt.index == ['FRA']
    assert cnt.lendingType.values[0] == 'XX'
