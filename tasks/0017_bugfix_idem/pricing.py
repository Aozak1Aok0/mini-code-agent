"""购物车计价。"""

PRICES = {"A": 3.0, "B": 5.0, "C": 2.5}


def unit_price(sku):
    return PRICES.get(sku, 1.0)


def cart_total(items):
    total = 0.0
    for it in items:
        total += unit_price(it["sku"]) * int(it["qty"])
    return round(total, 2)
