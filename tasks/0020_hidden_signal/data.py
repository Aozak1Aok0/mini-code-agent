"""构造确定性的测试数据。"""

import random


def make_events(n, users, seed=11):
    rng = random.Random(seed)
    return [
        {"user": users[rng.randrange(len(users))], "amount": round(rng.uniform(1, 200), 2)}
        for _ in range(n)
    ]


def make_users(n, prefix="u"):
    return [f"{prefix}{i:05d}" for i in range(n)]
