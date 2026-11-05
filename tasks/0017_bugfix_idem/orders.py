"""订单存储。"""

from dataclasses import dataclass, field


@dataclass
class Order:
    id: str
    key: str
    customer: str
    items: list
    total: float
    notes: list = field(default_factory=list)


class OrderStore:
    def __init__(self):
        self._by_key = {}
        self._seq = 0

    def find(self, key):
        return self._by_key.get(key)

    def create(self, key, customer, items, total):
        self._seq += 1
        order = Order(f"o{self._seq:04d}", key, customer, items, total)
        self._by_key[key] = order
        return order

    def all(self):
        return list(self._by_key.values())
