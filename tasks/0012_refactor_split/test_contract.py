from order import calc_total, format_receipt, parse_items


def test_parse_items():
    assert parse_items("pen,2.5,2") == [{"name": "pen", "price": 2.5, "qty": 2}]


def test_calc_total():
    items = [{"name": "pen", "price": 2.5, "qty": 2}]
    assert calc_total(items) == 5.0


def test_format_receipt():
    items = [{"name": "pen", "price": 2.5, "qty": 2}]
    assert format_receipt(items, 5.0) == "pen x2 = 5.00"
