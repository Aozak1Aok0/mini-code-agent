import pytest

from order import calc_total, format_receipt, parse_items, process_order


def test_empty_order():
    assert process_order("", 0.1) == {"items": [], "total": 0.0, "receipt": ""}


def test_parse_skips_blank_segments():
    assert parse_items("pen,2.5,2 ;; book,1,1") == [
        {"name": "pen", "price": 2.5, "qty": 2},
        {"name": "book", "price": 1.0, "qty": 1},
    ]


def test_format_multiline():
    items = [
        {"name": "a", "price": 1.0, "qty": 2},
        {"name": "b", "price": 2.0, "qty": 1},
    ]
    assert format_receipt(items, 4.0) == "a x2 = 2.00\nb x1 = 2.00"


def test_calc_total_float():
    assert calc_total([{"name": "x", "price": 0.1, "qty": 3}]) == pytest.approx(0.3)
