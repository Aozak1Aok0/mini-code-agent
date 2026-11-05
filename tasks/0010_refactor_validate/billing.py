"""账单计算（有重复的金额校验）。"""


def add_item(items, name, amount):
    if amount <= 0:
        raise ValueError("金额必须为正")
    if amount > 1000:
        raise ValueError("金额过大")
    items.append({"name": name, "amount": amount})


def apply_discount(amount, pct):
    if amount <= 0:
        raise ValueError("金额必须为正")
    if amount > 1000:
        raise ValueError("金额过大")
    return amount * (1 - pct / 100)
