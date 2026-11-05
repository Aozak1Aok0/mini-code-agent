# 任务 0008：实现分页

`paging.py` 里 `paginate()` 还是 `NotImplementedError`。

要求：页码从 1 开始，返回 `{"items": [...], "page": p, "total_pages": n}`。

- `total_pages` 向上取整，空列表为 0 页；
- 页码超出范围时 `items` 为空，但 `page` 原样返回；
- `page < 1` 或 `per_page < 1` 抛 `ValueError`。

约束：
- 只能改源码（`paging.py`），不能改 `test_paging.py`；
- 改完必须跑一次 `run_tests` 确认；
- 测试全绿后调用 `finish`。
