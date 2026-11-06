import time

from api import daily_report
from data import make_rows
from store import Store


def test_large_correct_and_fast():
    rows = make_rows(100000)
    ids = [r["id"] for r in rows[:20000]]
    store = Store(rows)
    t0 = time.perf_counter()
    out = daily_report(store, ids)
    elapsed = time.perf_counter() - t0
    assert len(out) == 20000
    assert out[ids[0]] == rows[0]["amount"]
    assert elapsed < 2.0, f"10 万行 / 2 万 id 用了 {elapsed:.2f}s"


def test_missing_ids_skipped():
    rows = make_rows(100)
    out = daily_report(Store(rows), ["nope", rows[3]["id"], "nope2"])
    assert list(out) == [rows[3]["id"]]


def test_duplicate_ids_do_not_break():
    rows = make_rows(100)
    rid = rows[9]["id"]
    out = daily_report(Store(rows), [rid, rid])
    assert out == {rid: rows[9]["amount"]}


def test_store_rows_still_readable():
    rows = make_rows(50)
    store = Store(rows)
    assert len(store.rows) == 50
    assert store.rows[0]["id"] == rows[0]["id"]


def test_empty_store():
    assert daily_report(Store([]), ["a", "b"]) == {}
