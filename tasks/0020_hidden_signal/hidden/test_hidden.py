import time

from api import report
from data import make_events, make_users


def _reference(events, users):
    out = {}
    for uid in users:
        total = 0.0
        for event in events:
            if event["user"] == uid:
                total += event["amount"]
        out[uid] = round(total, 2)
    return out


def test_matches_reference_on_random_data():
    users = make_users(400)
    events = make_events(3000, users)
    assert report(events, users) == _reference(events, users)


def test_unknown_users_are_ignored():
    users = ["a", "b"]
    events = [{"user": "a", "amount": 1.0}, {"user": "ghost", "amount": 999.0}]
    assert report(events, users) == {"a": 1.0, "b": 0.0}


def test_empty_users():
    assert report([{"user": "a", "amount": 1.0}], []) == {}


def test_daily_report_under_two_seconds():
    # 线上规模：20 万条事件、5 万个用户，SLO 2 秒
    users = make_users(50000)
    events = make_events(200000, users)
    t0 = time.perf_counter()
    out = report(events, users)
    elapsed = time.perf_counter() - t0
    assert len(out) == 50000
    assert elapsed < 2.0, f"日报聚合用了 {elapsed:.2f}s"
