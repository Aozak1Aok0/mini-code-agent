# 任务 0002：分块函数漏掉最后一段

`pytest -q` 会失败：`chunked()` 在列表长度不是 `size` 整数倍时漏掉最后一段。

约束：
- 只能改源码（`chunk.py`），不能改 `test_chunk.py`；
- 改完必须跑一次 `run_tests` 确认；
- 测试全绿后调用 `finish`。
