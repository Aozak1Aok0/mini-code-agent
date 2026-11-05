import storage
from report import summary


def setup_function():
    storage.reset()


def test_summary_empty():
    assert summary() == {"count": 0, "names": []}


def test_summary_after_add():
    storage.add("write")
    storage.add("read")
    assert summary() == {"count": 2, "names": ["write", "read"]}


def test_summary_after_delete():
    storage.add("write")
    rid = storage.add("read")
    storage.delete(rid)
    assert summary() == {"count": 1, "names": ["write"]}


def test_delete_unknown_is_noop():
    storage.add("write")
    storage.delete(999)
    assert summary()["count"] == 1


def test_add_after_delete_keeps_order():
    storage.add("a")
    rid = storage.add("b")
    storage.delete(rid)
    storage.add("c")
    assert summary()["names"] == ["a", "c"]
