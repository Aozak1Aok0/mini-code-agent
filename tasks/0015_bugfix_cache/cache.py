"""一个很小的记忆化装饰器。"""

_cache = {}


def cached(fn):
    def wrapper(*args, **kwargs):
        key = fn.__name__
        if key not in _cache:
            _cache[key] = fn(*args, **kwargs)
        return _cache[key]

    return wrapper
