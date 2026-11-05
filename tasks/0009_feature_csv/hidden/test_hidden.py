from csvloader import load_rows


def _write(tmp_path, text):
    p = tmp_path / "data.csv"
    p.write_text(text, encoding="utf-8")
    return p


def test_single_row(tmp_path):
    p = _write(tmp_path, "name,age\nada,3\n")
    assert load_rows(p) == [{"name": "ada", "age": "3"}]


def test_leading_zeros_stay_strings(tmp_path):
    p = _write(tmp_path, "id\n007\n")
    assert load_rows(p) == [{"id": "007"}]


def test_unicode_values(tmp_path):
    p = _write(tmp_path, "name\n张三\n")
    assert load_rows(p) == [{"name": "张三"}]


def test_column_order_kept(tmp_path):
    p = _write(tmp_path, "b,a\n2,1\n")
    assert list(load_rows(p)[0]) == ["b", "a"]
