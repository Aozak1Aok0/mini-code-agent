"""领域异常。"""


class InsufficientFunds(Exception):
    """余额不足。"""

    def __init__(self, account, balance, amount):
        super().__init__(f"{account} 余额 {balance} 不足以支出 {amount}")
        self.account = account
        self.balance = balance
        self.amount = amount
