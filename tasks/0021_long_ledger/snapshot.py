"""快照编解码。

v2 的字段：id / sku / qty / ts（ts 是 Unix 秒，int）。
v1 的字段：id / sku / q（数量）/ ts（"YYYY-MM-DD" 字符串）。
"""

import json

from models import Entry

VERSION = 2


def encode(store) -> str:
    return json.dumps(
        {"version": VERSION, "entries": [e.__dict__ for e in store.entries()]},
        ensure_ascii=False,
    )


def decode(payload):
    data = json.loads(payload) if isinstance(payload, str) else payload
    rows = data.get("entries", [])
    return [
        Entry(id=r["id"], sku=r["sku"], qty=r.get("qty", 0), ts=r.get("ts", 0))
        for r in rows
    ]
