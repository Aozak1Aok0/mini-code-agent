import pytest

from service import price


def test_kwargs_call():
    assert price(tier="basic") == 10
    assert price(tier="pro") == 30


def test_long_sequence():
    for tier, expected in [("basic", 10), ("pro", 30), ("basic", 10), ("pro", 30)]:
        assert price(tier) == expected


def test_error_then_other_tier():
    with pytest.raises(KeyError):
        price("missing")
    assert price("pro") == 30
