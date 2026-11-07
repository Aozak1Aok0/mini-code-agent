from replay import totals, totals_as_of
from snapshot import decode


def report(store) -> dict:
    return totals(store.entries())


def report_as_of(store, ts: int) -> dict:
    return totals_as_of(store.entries(), ts)


def load(payload) -> list:
    """从快照读回条目；v1 快照没有 version 字段，也要能读。"""
    return decode(payload)
