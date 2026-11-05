from settings import get_setting


def test_false_is_not_default():
    assert get_setting({"a": False}, "a", True) is False


def test_empty_string_is_not_default():
    assert get_setting({"a": ""}, "a", "fallback") == ""


def test_default_none():
    assert get_setting({}, "k", None) is None


def test_nested_value():
    assert get_setting({"a": {"b": 1}}, "a") == {"b": 1}
