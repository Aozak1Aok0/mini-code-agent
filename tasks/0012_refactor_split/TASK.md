# 任务 0012：拆长函数

`order.py` 的 `process_order()` 把解析、求和、排版挤在一个函数里。

要求：行为完全不变，拆成三个可单独调用的函数：
`parse_items(raw)`、`calc_total(items)`、`format_receipt(items, total)`，
`process_order` 只负责串起来。

`test_order.py` 必须保持全绿；`test_contract.py` 会检查三个函数存在且可单独调用。

约束：
- 只能改源码（`order.py`），不能改测试文件；
- 改完必须跑一次 `run_tests` 确认；
- 测试全绿后调用 `finish`。
