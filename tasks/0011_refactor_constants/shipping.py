"""运费计算（魔法数字版本）。"""


def shipping_fee(total, weight_kg):
    if total >= 800:
        return 0.0
    fee = max(5.0, weight_kg * 2.0)
    return round(fee * 1.13, 2)
