from api import Api


def test_replay_returns_same_order():
    api = Api()
    cart = [{"sku": "A", "qty": 2}]
    first = api.place("u1", cart)
    second = api.place("u1", cart)
    assert first.id == second.id
    assert api.count() == 1


def test_total_matches_prices():
    api = Api()
    order = api.place("u1", [{"sku": "A", "qty": 2}, {"sku": "B", "qty": 1}])
    assert order.total == 11.0


def test_different_carts_same_total():
    api = Api()
    one = api.place("u1", [{"sku": "A", "qty": 1}, {"sku": "B", "qty": 1}])
    two = api.place("u1", [{"sku": "A", "qty": 1}, {"sku": "C", "qty": 2}])
    assert one.total == two.total == 8.0
    assert one.id != two.id
    assert api.count() == 2
