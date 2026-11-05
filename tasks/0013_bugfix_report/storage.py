"""内存存储：按添加顺序保存待办。"""

_rows = {}
_order = []


def reset():
    _rows.clear()
    _order.clear()


def add(name):
    rid = len(_order) + 1
    _rows[rid] = {"id": rid, "name": name}
    _order.append(rid)
    return rid


def delete(rid):
    _rows.pop(rid, None)


def iter_rows():
    return [_rows[rid] for rid in _order]


def count():
    return len(_rows)
