from chunk import chunked


def test_size_one():
    assert chunked([1, 2, 3], 1) == [[1], [2], [3]]


def test_size_larger_than_list():
    assert chunked([1, 2], 10) == [[1, 2]]


def test_no_aliasing():
    out = chunked([1, 2, 3, 4], 2)
    assert out == [[1, 2], [3, 4]]
    assert out[0] is not out[1]
