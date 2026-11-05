"""下单编排：同一请求重放返回同一订单，不同购物车必须各自成单。"""

from keyer import request_key
from pricing import cart_total


class OrderService:
    def __init__(self, store):
        self.store = store

    def place(self, customer, items):
        total = cart_total(items)
        key = request_key(customer, total)
        existing = self.store.find(key)
        if existing is not None:
            return existing
        return self.store.create(key, customer, list(items), total)
