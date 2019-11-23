import pytest
import requests

try:
    from unittest import mock
except ImportError:
    import mock
from world_bank_data import get_countries


def assert_proxy_arg_in_get(*args, **kwargs):
    assert isinstance(kwargs.pop('proxies'), dict)
    return requests.get(*args, **kwargs)


@pytest.fixture
def proxies():
    return {'http': 'http://example.com:3128'}


def test_proxy_as_arg(proxies):
    with mock.patch('world_bank_data.request.get', assert_proxy_arg_in_get):
        get_countries(proxies=proxies)


def test_proxy_as_global_option(proxies):
    with mock.patch('world_bank_data.options.proxies', proxies):
        with mock.patch('world_bank_data.request.get', assert_proxy_arg_in_get):
            get_countries()
