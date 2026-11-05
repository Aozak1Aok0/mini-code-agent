# 任务 0009：实现 CSV 读取

`csvloader.py` 里 `load_rows()` 还是 `NotImplementedError`。

要求：第一行是表头，返回 `list[dict]`；空文件返回 `[]`；
数字字段保持字符串（不做类型推断）。

约束：
- 只能改源码（`csvloader.py`），不能改 `test_csvloader.py`；
- 改完必须跑一次 `run_tests` 确认；
- 测试全绿后调用 `finish`。
