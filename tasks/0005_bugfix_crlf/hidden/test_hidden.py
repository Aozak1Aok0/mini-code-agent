from textlines import lines


def test_mixed_endings():
    assert lines("a\r\nb\rc\n") == ["a", "b", "c"]


def test_only_newlines():
    assert lines("\n\n") == ["", ""]


def test_single_line_no_ending():
    assert lines("abc") == ["abc"]
