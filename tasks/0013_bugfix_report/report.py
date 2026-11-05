"""把存储里的待办汇总成列表页要的结构。"""

from storage import count, iter_rows


def summary():
    return {"count": count(), "names": [row["name"] for row in iter_rows()]}
