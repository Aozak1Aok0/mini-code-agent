"""请求去重键：同一个请求重放时返回同一个订单。"""

import hashlib


def request_key(customer, total):
    raw = f"{customer}:{total}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
