"""把一条记录格式化成 CSV 行。"""


def row_text(item):
    return f"{item['name']},{item['qty']}"
