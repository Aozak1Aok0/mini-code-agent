def totals(entries) -> dict:
    """按 sku 汇总数量。"""
    out = {}
    for e in entries:
        out[e.sku] = out.get(e.sku, 0) + e.qty
    return out


def totals_as_of(entries, ts: int) -> dict:
    """只汇总 ts 之前（含）的条目。"""
    out = {}
    for e in entries:
        if e.ts <= ts:
            out[e.sku] = out.get(e.sku, 0) + e.qty
    return out
