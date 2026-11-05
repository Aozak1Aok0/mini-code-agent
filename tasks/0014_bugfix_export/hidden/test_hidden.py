from exporter import export


def test_three_exports(tmp_path):
    for i in range(3):
        p = tmp_path / f"{i}.csv"
        export([{"name": f"n{i}", "qty": i}], p)
        assert p.read_text(encoding="utf-8") == f"n{i},{i}"


def test_export_after_empty(tmp_path):
    export([], tmp_path / "empty.csv")
    p = tmp_path / "one.csv"
    export([{"name": "a", "qty": 1}], p)
    assert p.read_text(encoding="utf-8") == "a,1"
