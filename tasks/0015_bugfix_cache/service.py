"""业务侧：按档位取价格。"""

from cache import cached


@cached
def price(tier):
    return {"basic": 10, "pro": 30}[tier]
