from shipping import shipping_fee


def test_threshold_boundary_free():
    assert shipping_fee(800, 0) == 0.0


def test_just_below_threshold():
    assert shipping_fee(799.99, 1) == 5.65


def test_heavy_parcel():
    assert shipping_fee(10, 10) == 22.6
