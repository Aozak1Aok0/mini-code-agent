from textlines import lines


def test_lf():
    assert lines("a\nb") == ["a", "b"]


def test_crlf():
    assert lines("a\r\nb\r\n") == ["a", "b"]


def test_trailing_blank():
    assert lines("a\n\n") == ["a", ""]


def test_empty():
    assert lines("") == []
