"""内存账户表。

余额放在 `Account` 里；另有一份 `_snapshot` 给校验层读，
只有显式调用 `refresh()` 时才会同步。这样设计是为了让一次批量操作
看到一致的余额视图。
"""

from models import Account


class Store:
    def __init__(self, balances):
        self._accounts = {
            name: Account(name, float(amount)) for name, amount in balances.items()
        }
        self._snapshot = {name: float(amount) for name, amount in balances.items()}

    def refresh(self):
        """把快照同步到当前余额。"""
        self._snapshot = {name: acc.balance for name, acc in self._accounts.items()}

    def balances(self):
        """校验层读到的余额视图。"""
        return dict(self._snapshot)

    def account(self, name):
        if name not in self._accounts:
            raise KeyError(name)
        return self._accounts[name]

    def all(self):
        return list(self._accounts.values())
