"""订单处理（三段逻辑挤在一起）。"""


def process_order(raw, tax_rate):
    items = []
    for line in raw.split(";"):
        line = line.strip()
        if not line:
            continue
        name, price, qty = line.split(",")
        items.append({"name": name, "price": float(price), "qty": int(qty)})
    subtotal = 0.0
    for it in items:
        subtotal += it["price"] * it["qty"]
    total = round(subtotal * (1 + tax_rate), 2)
    lines = [f"{it['name']} x{it['qty']} = {it['price'] * it['qty']:.2f}" for it in items]
    return {"items": items, "total": total, "receipt": "\n".join(lines)}
