from paging import paginate


def test_exact_boundary():
    out = paginate([1, 2, 3, 4], 2, 2)
    assert out["items"] == [3, 4]
    assert out["total_pages"] == 2


def test_per_page_larger_than_list():
    assert paginate([1, 2], 1, 99)["total_pages"] == 1


def test_items_are_same_objects():
    xs = [{"id": 1}, {"id": 2}]
    assert paginate(xs, 1, 10)["items"][0] is xs[0]


def test_input_not_mutated():
    xs = [1, 2, 3]
    paginate(xs, 1, 2)
    assert xs == [1, 2, 3]
