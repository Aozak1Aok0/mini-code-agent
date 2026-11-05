import pytest

from api import make_api
from errors import InsufficientFunds


def test_transfer_moves_money():
    api = make_api({"a": 100.0, "b": 0.0})
    out = api.transfer("a", "b", 30)
    assert out == {"src": 70.0, "dst": 30.0}
    assert api.balance("b") == 30.0


def test_transfer_more_than_balance_rejected():
    api = make_api({"a": 10.0, "b": 0.0})
    with pytest.raises(InsufficientFunds):
        api.transfer("a", "b", 11)


def test_two_transfers_cannot_overdraw():
    api = make_api({"a": 50.0, "b": 0.0})
    api.transfer("a", "b", 30)
    with pytest.raises(InsufficientFunds):
        api.transfer("a", "b", 30)
    assert api.balance("a") >= 0
