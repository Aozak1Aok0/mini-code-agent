import pytest

from duration import parse_duration


def test_hours_minutes():
    assert parse_duration("1h30m") == 5400


def test_seconds():
    assert parse_duration("45s") == 45


def test_mixed_order():
    assert parse_duration("30m1h") == 5400


def test_repeat_units():
    assert parse_duration("1h1h") == 7200


def test_empty():
    with pytest.raises(ValueError):
        parse_duration("")


def test_garbage():
    with pytest.raises(ValueError):
        parse_duration("abc")
