"""对外接口。"""

import report


def daily_report(store, ids):
    """返回 {id: amount}，缺失的 id 不进结果。"""
    return report.totals(store, ids)
