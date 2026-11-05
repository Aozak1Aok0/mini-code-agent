"""把序列切成固定大小的小块。"""


def chunked(xs, size):
    """按 size 切分，最后不足 size 的一段也要保留。"""
    if size <= 0:
        raise ValueError("size 必须为正")
    return [xs[i:i + size] for i in range(0, len(xs) - size, size)]
