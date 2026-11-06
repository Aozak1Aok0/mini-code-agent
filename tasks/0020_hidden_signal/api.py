"""对外接口。"""

import aggregate


def report(events, users):
    """返回 {user: 金额}，键的顺序与 users 一致，金额保留两位小数。"""
    return aggregate.daily_totals(events, users)
