from order import process_order


def test_basic():
    raw = "pen,2.5,2; book,10,1"
    out = process_order(raw, 0.1)
    assert out["total"] == 16.5
    assert out["receipt"].splitlines() == ["pen x2 = 5.00", "book x1 = 10.00"]


def test_blank_segments():
    out = process_order(" pen,1,1 ;; ", 0.0)
    assert out["total"] == 1.0
