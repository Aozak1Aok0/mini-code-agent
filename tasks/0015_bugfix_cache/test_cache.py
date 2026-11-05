import pytest

from service import price


def test_different_args():
    assert price("basic") == 10
    assert price("pro") == 30


def test_same_arg_is_stable():
    assert price("pro") == 30
    assert price("pro") == 30


def test_error_does_not_poison_cache():
    with pytest.raises(KeyError):
        price("missing")
    assert price("basic") == 10
