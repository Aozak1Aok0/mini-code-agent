import shipping


def test_constants():
    assert shipping.FREE_SHIPPING_THRESHOLD == 800
    assert shipping.BASE_FEE == 5.0
    assert shipping.TAX_RATE == 0.13
