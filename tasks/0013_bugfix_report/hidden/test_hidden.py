import storage
from report import summary


def setup_function():
    storage.reset()


def test_delete_all_then_add():
    a = storage.add("a")
    b = storage.add("b")
    storage.delete(a)
    storage.delete(b)
    assert summary() == {"count": 0, "names": []}
    storage.add("c")
    assert summary() == {"count": 1, "names": ["c"]}


def test_delete_first():
    storage.add("a")
    storage.add("b")
    storage.delete(1)
    assert summary()["names"] == ["b"]


def test_many_cycles():
    for i in range(5):
        rid = storage.add(f"t{i}")
        storage.delete(rid)
    assert summary()["count"] == 0
