import pytest

from billing import add_item, apply_discount


def test_add_item():
    items = []
    add_item(items, "pen", 12.5)
    assert items == [{"name": "pen", "amount": 12.5}]


def test_add_rejects_non_positive():
    with pytest.raises(ValueError):
        add_item([], "pen", 0)


def test_add_rejects_too_large():
    with pytest.raises(ValueError):
        add_item([], "pen", 1001)


def test_discount():
    assert apply_discount(100, 10) == 90


def test_discount_checks():
    with pytest.raises(ValueError):
        apply_discount(-1, 10)
    with pytest.raises(ValueError):
        apply_discount(2000, 10)
