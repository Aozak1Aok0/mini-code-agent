from api import Api


def test_key_is_stable_across_dict_order():
    api = Api()
    a = api.place("u1", [{"sku": "A", "qty": 1}])
    b = api.place("u1", [{"qty": 1, "sku": "A"}])
    assert a.id == b.id
    assert api.count() == 1


def test_quantity_change_makes_new_order():
    api = Api()
    a = api.place("u1", [{"sku": "A", "qty": 1}, {"sku": "B", "qty": 1}])
    b = api.place("u1", [{"sku": "A", "qty": 2}, {"sku": "B", "qty": 1}])
    assert a.id != b.id
    assert api.count() == 2


def test_customer_isolation():
    api = Api()
    a = api.place("u1", [{"sku": "A", "qty": 1}])
    b = api.place("u2", [{"sku": "A", "qty": 1}])
    assert a.id != b.id


def test_replay_returns_same_object():
    api = Api()
    cart = [{"sku": "A", "qty": 1}]
    first = api.place("u1", cart)
    second = api.place("u1", cart)
    assert first is second
