"""报表：按 id 取行。"""


def totals(store, ids):
    out = {}
    for rid in ids:
        for row in store.rows:
            if row["id"] == rid:
                out[rid] = row["amount"]
                break
    return out
