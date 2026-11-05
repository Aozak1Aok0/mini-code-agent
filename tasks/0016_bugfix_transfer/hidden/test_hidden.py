import pytest

from api import make_api
from errors import InsufficientFunds


def test_failed_transfer_leaves_no_trace():
    api = make_api({"a": 30.0, "b": 0.0})
    with pytest.raises(InsufficientFunds):
        api.transfer("a", "b", 50)
    assert api.balance("a") == 30.0
    assert api.balance("b") == 0.0
    assert api.entries("a") == []


def test_unknown_target_does_not_debit_source():
    api = make_api({"a": 30.0})
    with pytest.raises(KeyError):
        api.transfer("a", "nobody", 10)
    assert api.balance("a") == 30.0


def test_can_empty_account():
    api = make_api({"a": 10.0, "b": 0.0})
    out = api.transfer("a", "b", 10)
    assert out == {"src": 0.0, "dst": 10.0}


def test_entries_recorded_per_account():
    api = make_api({"a": 10.0, "b": 0.0})
    api.transfer("a", "b", 4)
    assert [e.delta for e in api.entries("a")] == [-4.0]
    assert [e.delta for e in api.entries("b")] == [4.0]


def test_zero_amount_rejected():
    api = make_api({"a": 10.0, "b": 0.0})
    with pytest.raises(ValueError):
        api.transfer("a", "b", 0)
