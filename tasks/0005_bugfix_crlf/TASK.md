# 任务 0005：Windows 换行残留

`pytest -q` 会失败：`lines()` 按 `\n` 切分，遇到 `\r\n` 时每行结尾多一个 `\r`，
末尾空行也没去掉。

约束：
- 只能改源码（`textlines.py`），不能改 `test_textlines.py`；
- 改完必须跑一次 `run_tests` 确认；
- 测试全绿后调用 `finish`。
