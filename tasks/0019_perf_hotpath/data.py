"""构造确定性的测试数据。"""

import random


def make_rows(n, seed=7):
    rng = random.Random(seed)
    return [
        {"id": f"u{i:06d}", "amount": rng.randint(1, 500), "region": rng.choice(["n", "s", "e", "w"])}
        for i in range(n)
    ]
