from slug import slugify


def test_punctuation():
    assert slugify("Hello, World!") == "hello-world"


def test_spaces():
    assert slugify("  A   B  ") == "a-b"


def test_digits():
    assert slugify("v1.2 Release") == "v1-2-release"


def test_empty():
    assert slugify("") == ""
