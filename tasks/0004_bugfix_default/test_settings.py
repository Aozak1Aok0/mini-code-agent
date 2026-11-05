from settings import get_setting


def test_present():
    assert get_setting({"a": 1}, "a") == 1


def test_missing_with_default():
    assert get_setting({}, "timeout", 30) == 30


def test_missing_without_default():
    assert get_setting({}, "missing") is None


def test_falsy_value_is_not_default():
    assert get_setting({"a": 0}, "a", 30) == 0
