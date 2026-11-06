import time

from api import daily_report
from data import make_rows
from store import Store


def test_small_correct():
    rows = make_rows(10)
    store = Store(rows)
    ids = [rows[0]["id"], rows[5]["id"], "nope"]
    assert daily_report(store, ids) == {rows[0]["id"]: rows[0]["amount"], rows[5]["id"]: rows[5]["amount"]}


def test_empty_ids():
    assert daily_report(Store(make_rows(10)), []) == {}


def test_report_is_fast():
    # 线上规模：10 万行、每次 2 万个 id，SLO 1 秒
    rows = make_rows(100000)
    ids = [r["id"] for r in rows[:20000]]
    t0 = time.perf_counter()
    out = daily_report(Store(rows), ids)
    elapsed = time.perf_counter() - t0
    assert len(out) == 20000
    assert elapsed < 1.5, f"报表太慢：{elapsed:.2f}s"
