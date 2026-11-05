from exporter import export


def test_single_export(tmp_path):
    p = tmp_path / "one.csv"
    export([{"name": "pen", "qty": 2}], p)
    assert p.read_text(encoding="utf-8") == "pen,2"


def test_two_exports_are_independent(tmp_path):
    export([{"name": "pen", "qty": 2}], tmp_path / "one.csv")
    second = tmp_path / "two.csv"
    export([{"name": "book", "qty": 1}], second)
    assert second.read_text(encoding="utf-8") == "book,1"


def test_empty_export(tmp_path):
    p = tmp_path / "empty.csv"
    export([], p)
    assert p.read_text(encoding="utf-8") == ""
