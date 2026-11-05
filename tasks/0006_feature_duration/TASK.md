# 任务 0006：实现 parse_duration

`duration.py` 里 `parse_duration()` 还是 `NotImplementedError`。

要求：把 `"1h30m"` 这类时长解析成秒数。

- 支持 `h` / `m` / `s`，可任意组合、可乱序、可重复（累加）；
- 空串或无法识别的输入抛 `ValueError`；
- 不支持小数。

约束：
- 只能改源码（`duration.py`），不能改 `test_duration.py`；
- 改完必须跑一次 `run_tests` 确认；
- 测试全绿后调用 `finish`。
