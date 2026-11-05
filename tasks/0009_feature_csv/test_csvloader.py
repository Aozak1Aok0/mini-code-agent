import csv
import io

from csvloader import load_rows


def _write(tmp_path, text):
    p = tmp_path / "data.csv"
    p.write_text(text, encoding="utf-8")
    return p


def test_two_rows(tmp_path):
    p = _write(tmp_path, "name,age\nada,3\nbob,5\n")
    assert load_rows(p) == [{"name": "ada", "age": "3"}, {"name": "bob", "age": "5"}]


def test_empty_file(tmp_path):
    p = _write(tmp_path, "")
    assert load_rows(p) == []


def test_header_only(tmp_path):
    p = _write(tmp_path, "name,age\n")
    assert load_rows(p) == []
