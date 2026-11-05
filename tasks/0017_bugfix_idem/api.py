"""对外门面。"""

from orders import OrderStore
from service import OrderService


class Api:
    def __init__(self):
        self.store = OrderStore()
        self.service = OrderService(self.store)

    def place(self, customer, items):
        return self.service.place(customer, items)

    def order(self, order_id):
        for order in self.store.all():
            if order.id == order_id:
                return order
        raise KeyError(order_id)

    def count(self):
        return len(self.store.all())
