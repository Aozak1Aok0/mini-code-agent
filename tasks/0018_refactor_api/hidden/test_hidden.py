import orders_a
import orders_b
import pricing
from api import both, quote


def _cart(*pairs):
    return [{"price": p, "qty": q} for p, q in pairs]


def test_half_up_and_banker_still_differ():
    items = _cart((2.5, 1))
    assert quote(items, "a") == 3
    assert quote(items, "b") == 2


def test_three_point_five_agrees():
    items = _cart((3.5, 1))
    assert quote(items, "a") == 4
    assert quote(items, "b") == 4


def test_old_modules_still_work_alone():
    items = _cart((2.0, 2), (1.0, 1))
    assert orders_a.total(items) == 5
    assert orders_b.total(items) == 5


def test_core_matches_old_modules():
    items = _cart((2.5, 1), (0.5, 1))
    assert pricing.total(items, "half_up") == orders_a.total(items)
    assert pricing.total(items, "banker") == orders_b.total(items)


def test_sum_items_does_not_round():
    assert pricing.sum_items(_cart((2.5, 1))) == 2.5
    assert pricing.sum_items([]) == 0


def test_unknown_mode_raises():
    try:
        pricing.total(_cart((1.0, 1)), "ceil")
    except ValueError:
        return
    raise AssertionError("未知 mode 应抛 ValueError")


def test_both_versions_via_api():
    items = _cart((2.5, 1))
    assert both(items) == {"a": 3, "b": 2}
