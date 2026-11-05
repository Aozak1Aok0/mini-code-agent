import pytest

from billing import MAX_AMOUNT, add_item, apply_discount, validate_amount


def test_validate_boundary_allowed():
    validate_amount(MAX_AMOUNT)


def test_add_boundary_allowed():
    items = []
    add_item(items, "pen", 1000.0)
    assert items == [{"name": "pen", "amount": 1000.0}]


def test_add_does_not_append_on_error():
    items = []
    with pytest.raises(ValueError):
        add_item(items, "pen", -1)
    assert items == []


def test_discount_zero_pct():
    assert apply_discount(1000, 0) == 1000
