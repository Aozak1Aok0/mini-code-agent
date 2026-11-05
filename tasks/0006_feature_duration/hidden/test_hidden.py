import pytest

from duration import parse_duration


def test_all_units():
    assert parse_duration("1h30m15s") == 5415


def test_zero():
    assert parse_duration("0s") == 0


def test_missing_unit():
    with pytest.raises(ValueError):
        parse_duration("10")


def test_decimal_rejected():
    with pytest.raises(ValueError):
        parse_duration("1.5h")


def test_unit_only():
    with pytest.raises(ValueError):
        parse_duration("h")
