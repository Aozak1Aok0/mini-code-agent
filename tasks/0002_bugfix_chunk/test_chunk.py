from chunk import chunked


def test_even():
    assert chunked([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]


def test_remainder():
    assert chunked([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]


def test_shorter_than_size():
    assert chunked([1], 3) == [[1]]


def test_empty():
    assert chunked([], 3) == []


def test_bad_size():
    import pytest

    with pytest.raises(ValueError):
        chunked([1], 0)
