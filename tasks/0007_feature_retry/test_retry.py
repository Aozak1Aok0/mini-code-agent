import pytest

from retry import retry


def test_eventually_succeeds():
    calls = {"n": 0}

    @retry(times=3)
    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise ValueError("boom")
        return "ok"

    assert flaky() == "ok"
    assert calls["n"] == 3


def test_gives_up():
    calls = {"n": 0}

    @retry(times=2)
    def always_fail():
        calls["n"] += 1
        raise ValueError("boom")

    with pytest.raises(ValueError):
        always_fail()
    assert calls["n"] == 3


def test_other_errors_pass_through():
    calls = {"n": 0}

    @retry(times=5)
    def wrong_type():
        calls["n"] += 1
        raise TypeError("nope")

    with pytest.raises(TypeError):
        wrong_type()
    assert calls["n"] == 1
