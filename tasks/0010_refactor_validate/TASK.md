# 任务 0010：抽出重复校验

`billing.py` 里 `add_item()` 和 `apply_discount()` 各写了一遍相同的金额校验。

要求：行为完全不变，把校验抽成 `validate_amount(amount)`，并把上限提成常量
`MAX_AMOUNT = 1000.0`。

`test_billing.py` 必须保持全绿；`test_contract.py` 会检查新接口存在。

约束：
- 只能改源码（`billing.py`），不能改测试文件；
- 改完必须跑一次 `run_tests` 确认；
- 测试全绿后调用 `finish`。
