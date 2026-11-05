import pricing


def test_sum_items():
    assert pricing.sum_items([{"price": 1.5, "qty": 2}]) == 3.0


def test_total_half_up():
    assert pricing.total([{"price": 2.5, "qty": 1}], "half_up") == 3


def test_total_banker():
    assert pricing.total([{"price": 2.5, "qty": 1}], "banker") == 2
