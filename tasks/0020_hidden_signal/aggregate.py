"""日报聚合：按用户汇总金额。"""


def daily_totals(events, users):
    out = {}
    for uid in users:
        total = 0.0
        for event in events:
            if event["user"] == uid:
                total += event["amount"]
        out[uid] = round(total, 2)
    return out
