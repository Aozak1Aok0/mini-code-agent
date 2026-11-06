from api import report
from data import make_events, make_users


def test_totals_match_hand_computed():
    events = [
        {"user": "a", "amount": 10.5},
        {"user": "b", "amount": 3.0},
        {"user": "a", "amount": 2.25},
    ]
    assert report(events, ["a", "b", "c"]) == {"a": 12.75, "b": 3.0, "c": 0.0}


def test_key_order_follows_users():
    events = make_events(50, ["x", "y", "z"])
    users = ["z", "y", "x"]
    assert list(report(events, users)) == users


def test_empty_events():
    assert report([], ["a", "b"]) == {"a": 0.0, "b": 0.0}
