from dataclasses import dataclass


@dataclass
class Entry:
    id: str
    sku: str
    qty: int
    ts: int
