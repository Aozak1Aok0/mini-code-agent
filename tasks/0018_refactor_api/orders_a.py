"""旧版结算 A：.5 一律进位（四舍五入）。"""


def total(items):
    raw = sum(it["price"] * it["qty"] for it in items)
    # 加一个极小量，避免 2.4999999 这类浮点误差
    return int(raw + 0.5 + 1e-9)
