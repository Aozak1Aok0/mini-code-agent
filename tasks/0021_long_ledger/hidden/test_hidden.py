"""隐藏测试：v1 备份的迁移与按时间过滤。

只依赖 TASK.md 里写明的行为，不引入新要求。
"""

import json

from api import load, report, report_as_of
from migrate import migrate_v1
from snapshot import decode
from store import Store

V1 = {
    "version": 1,
    "entries": [
        {"id": "e1", "sku": "A", "q": 3, "ts": "2026-01-01"},
        {"id": "e2", "sku": "B", "q": 1, "ts": "2026-01-02"},
        {"id": "e3", "sku": "A", "q": -1, "ts": "2026-01-03"},
    ],
}

E_0102 = 1767312000
E_0103 = 1767398400


def test_migrate_is_idempotent():
    once = migrate_v1(V1)
    twice = migrate_v1(once)
    assert once == twice


def test_migrate_converts_ts_to_epoch():
    rows = migrate_v1(V1)["entries"]
    assert rows[0]["ts"] == 1767225600
    assert all(isinstance(r["ts"], int) for r in rows)


def test_load_keeps_quantity_and_epoch():
    entries = load(json.dumps(V1))
    assert [e.qty for e in entries] == [3, 1, -1]
    assert all(isinstance(e.ts, int) for e in entries)


def test_legacy_report_keeps_negative_qty():
    assert report(Store(load(V1))) == {"A": 2, "B": 1}


def test_legacy_as_of_uses_epoch():
    store = Store(load(V1))
    assert report_as_of(store, E_0102) == {"A": 3, "B": 1}
    assert report_as_of(store, E_0103) == {"A": 2, "B": 1}


def test_legacy_reencode_roundtrip():
    store = Store(load(V1))
    assert report(Store(decode(json.dumps({"version": 2, "entries": [e.__dict__ for e in store.entries()]})))) == {"A": 2, "B": 1}


def test_v2_snapshot_untouched():
    assert decode({"version": 2, "entries": [{"id": "x", "sku": "C", "qty": 7, "ts": 10}]})[
        0
    ].qty == 7
