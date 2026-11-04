"""一些统计函数（仓库里有 bug，等 agent 来修）。"""


def mean(xs):
    return sum(xs) / len(xs)


def median(xs):
    xs = sorted(xs)
    n = len(xs)
    mid = n // 2
    if n % 2:
        return xs[mid]
    return (xs[mid - 1] + xs[mid]) / 2
