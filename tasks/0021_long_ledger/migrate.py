"""v1 → v2 快照迁移。"""

from datetime import datetime, timezone


def _ts_to_epoch(value):
    if isinstance(value, (int, float)):
        return int(value)
    return int(datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp())


def migrate_v1(data: dict) -> dict:
    rows = []
    for r in data.get("entries", []):
        rows.append(
            {
                "id": r["id"],
                "sku": r["sku"],
                "qty": r.get("qty", r.get("q", 0)),
                "ts": r.get("ts", 0),
            }
        )
    return {"version": 2, "entries": rows}
