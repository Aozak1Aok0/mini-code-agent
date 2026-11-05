import pytest

from paging import paginate


def test_first_page():
    assert paginate(list(range(7)), 1, 3) == {"items": [0, 1, 2], "page": 1, "total_pages": 3}


def test_last_partial_page():
    assert paginate(list(range(7)), 3, 3) == {"items": [6], "page": 3, "total_pages": 3}


def test_out_of_range():
    assert paginate([1, 2], 5, 2) == {"items": [], "page": 5, "total_pages": 1}


def test_empty():
    assert paginate([], 1, 10)["total_pages"] == 0


def test_bad_page():
    with pytest.raises(ValueError):
        paginate([1], 0, 1)


def test_bad_size():
    with pytest.raises(ValueError):
        paginate([1], 1, 0)
