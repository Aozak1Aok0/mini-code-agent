"""账户与流水模型。"""

from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class Entry:
    """一条流水。"""

    account: str
    delta: float
    memo: str = ""


@dataclass
class Account:
    """账户：余额 + 流水。"""

    name: str
    balance: float
    entries: List[Entry] = field(default_factory=list)

    def apply(self, entry: Entry) -> None:
        self.balance = round(self.balance + entry.delta, 2)
        self.entries.append(entry)
