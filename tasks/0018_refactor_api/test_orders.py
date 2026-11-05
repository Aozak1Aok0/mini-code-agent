from api import both, quote


def test_quote_rounds_like_before():
    items = [{"price": 2.0, "qty": 3}, {"price": 1.0, "qty": 2}]
    assert quote(items) == 8
    assert quote(items, "b") == 8


def test_both_versions_exist():
    items = [{"price": 10.0, "qty": 1}]
    assert both(items) == {"a": 10, "b": 10}


def test_empty_cart():
    assert quote([], "a") == 0
    assert quote([], "b") == 0
