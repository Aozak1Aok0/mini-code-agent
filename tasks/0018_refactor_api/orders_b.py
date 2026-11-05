"""旧版结算 B：.5 取偶（银行家舍入）。"""


def total(items):
    raw = sum(it["price"] * it["qty"] for it in items)
    return int(round(raw))
