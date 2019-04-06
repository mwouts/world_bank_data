import re
import mock
from world_bank_data import search_countries


def test_language():
    assert search_countries(re.compile('ES')).name[0] == 'Spain'
    assert search_countries(re.compile('ES'), language='es').name[0] == 'España'


def test_language_through_options():
    assert search_countries(re.compile('ES')).name[0] == 'Spain'
    with mock.patch('world_bank_data.options.language', 'es'):
        assert search_countries(re.compile('ES')).name[0] == 'España'
