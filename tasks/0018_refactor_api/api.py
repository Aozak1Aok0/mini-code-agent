"""对外门面：两个版本并存。"""

import orders_a
import orders_b


def quote(items, version="a"):
    if version == "a":
        return orders_a.total(items)
    if version == "b":
        return orders_b.total(items)
    raise ValueError(f"未知版本: {version}")


def both(items):
    return {"a": orders_a.total(items), "b": orders_b.total(items)}
