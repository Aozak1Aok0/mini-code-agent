"""对外门面：把 store 和 service 接起来。"""

from service import TransferService
from store import Store


class Api:
    def __init__(self, store):
        self.store = store
        self.service = TransferService(store)

    def transfer(self, src, dst, amount, memo=""):
        return self.service.transfer(src, dst, amount, memo)

    def balance(self, name):
        return self.store.account(name).balance

    def entries(self, name):
        return list(self.store.account(name).entries)


def make_api(balances):
    return Api(Store(balances))
