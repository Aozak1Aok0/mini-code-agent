import pytest

from retry import retry


def test_zero_retries():
    calls = {"n": 0}

    @retry(times=0)
    def boom():
        calls["n"] += 1
        raise ValueError("x")

    with pytest.raises(ValueError):
        boom()
    assert calls["n"] == 1


def test_success_is_not_retried():
    calls = {"n": 0}

    @retry(times=5)
    def ok():
        calls["n"] += 1
        return 7

    assert ok() == 7
    assert calls["n"] == 1


def test_args_forwarded():
    @retry(times=1)
    def add(a, b=0):
        return a + b

    assert add(1, b=2) == 3


def test_raises_last_exception():
    seen = {"n": 0}

    @retry(times=2)
    def f():
        seen["n"] += 1
        raise ValueError(str(seen["n"]))

    with pytest.raises(ValueError) as err:
        f()
    assert str(err.value) == "3"
