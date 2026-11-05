"""把记录导出成 CSV 文件。"""

from formatter import row_text

_buffer = []


def export(items, path):
    for item in items:
        _buffer.append(row_text(item))
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(_buffer))
