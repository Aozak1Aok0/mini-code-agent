import json

from api import load, report, report_as_of
from models import Entry
from replay import totals, totals_as_of
from snapshot import decode, encode
from store import Store

V1 = {
    "version": 1,
    "entries": [
        {"id": "e1", "sku": "A", "q": 3, "ts": "2026-01-01"},
        {"id": "e2", "sku": "B", "q": 1, "ts": "2026-01-02"},
        {"id": "e3", "sku": "A", "q": -1, "ts": "2026-01-03"},
    ],
}

V1_EPOCH_0102 = 1767312000
V1_EPOCH_0103 = 1767398400


def test_fresh_store_totals():
    store = Store([Entry("e1", "A", 2, 100), Entry("e2", "A", 3, 200)])
    assert report(store) == {"A": 5}


def test_v2_roundtrip():
    store = Store([Entry("e1", "A", 4, 100)])
    restored = decode(encode(store))
    assert report(Store(restored)) == {"A": 4}
    assert restored[0].ts == 100


def test_totals_as_of():
    entries = [Entry("e1", "A", 2, 100), Entry("e2", "A", 5, 200)]
    assert totals_as_of(entries, 150) == {"A": 2}
    assert totals_as_of(entries, 250) == {"A": 7}


def test_negative_qty_is_a_return():
    store = Store([Entry("e1", "A", 3, 100), Entry("e2", "A", -1, 200)])
    assert report(store) == {"A": 2}


def test_legacy_snapshot_totals():
    store = Store(load(json.dumps(V1)))
    assert report(store) == {"A": 2, "B": 1}


def test_legacy_snapshot_as_of():
    store = Store(load(V1))
    assert report_as_of(store, V1_EPOCH_0102) == {"A": 3, "B": 1}
    assert report_as_of(store, V1_EPOCH_0103) == {"A": 2, "B": 1}


def test_load_accepts_dict_and_str():
    assert len(load(V1)) == 3
    assert len(load(json.dumps(V1))) == 3


def test_totals_ignores_empty():
    assert totals([]) == {}
