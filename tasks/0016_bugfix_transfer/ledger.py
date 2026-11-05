"""记账：先校验，再落账。"""

from errors import InsufficientFunds
from models import Entry


def post(store, account, delta, memo=""):
    """给账户记一笔；余额不足抛 InsufficientFunds。"""
    balances = store.balances()
    if account not in balances:
        raise KeyError(account)
    if balances[account] + delta < 0:
        raise InsufficientFunds(account, balances[account], -delta)

    target = store.account(account)
    target.apply(Entry(account, delta, memo))
    return target.balance
