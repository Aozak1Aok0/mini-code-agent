"""转账编排。"""

from ledger import post


class TransferService:
    def __init__(self, store):
        self.store = store

    def transfer(self, src, dst, amount, memo=""):
        if amount <= 0:
            raise ValueError("金额必须为正")
        if src == dst:
            raise ValueError("不能转给自己")

        post(self.store, src, -amount, memo)
        post(self.store, dst, amount, memo)
        return {
            "src": self.store.account(src).balance,
            "dst": self.store.account(dst).balance,
        }
