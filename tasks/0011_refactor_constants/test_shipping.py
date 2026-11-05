from shipping import shipping_fee


def test_free_over_threshold():
    assert shipping_fee(800, 10) == 0.0


def test_base_fee_floor():
    assert shipping_fee(10, 0.5) == 5.65


def test_weight_scales():
    assert shipping_fee(10, 3) == 6.78
