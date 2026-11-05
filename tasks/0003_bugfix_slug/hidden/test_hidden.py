from slug import slugify


def test_repeated_separators_fold():
    assert slugify("A--B") == "a-b"


def test_underscore_is_separator():
    assert slugify("A_B") == "a-b"


def test_only_punctuation():
    assert slugify("!!!") == ""


def test_tabs_and_spaces():
    assert slugify("hello\tworld") == "hello-world"
