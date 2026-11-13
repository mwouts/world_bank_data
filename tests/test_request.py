from unittest.mock import Mock

from world_bank_data.request import wb_get


def test_pagination_preserves_parameters_and_proxy(monkeypatch):
    calls = []
    pages = [
        [{"page": 1, "pages": 2}, [{"id": "first"}]],
        [{"page": 2, "pages": 2}, [{"id": "second"}]],
    ]

    def get(**kwargs):
        calls.append({**kwargs, "params": kwargs["params"].copy()})
        return Mock(json=Mock(return_value=pages[len(calls) - 1]))

    monkeypatch.setattr("world_bank_data.request.get", get)
    proxies = {"https": "http://proxy.example:3128"}
    assert wb_get("indicator", proxies=proxies, per_page=1) == [
        {"id": "first"},
        {"id": "second"},
    ]
    assert [call["params"].get("page") for call in calls] == [None, 2]
    assert all(call["params"]["per_page"] == 1 for call in calls)
    assert all(call["proxies"] == proxies for call in calls)


def test_malformed_api_error_is_reported(monkeypatch):
    import pytest

    response = Mock(json=Mock(return_value=[{"message": []}]))
    monkeypatch.setattr("world_bank_data.request.get", Mock(return_value=response))
    with pytest.raises(ValueError, match="message"):
        wb_get("indicator")
