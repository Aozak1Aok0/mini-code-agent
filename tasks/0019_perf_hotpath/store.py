"""内存存储：报表数据都从这里读。"""


class Store:
    def __init__(self, rows):
        self.rows = list(rows)
