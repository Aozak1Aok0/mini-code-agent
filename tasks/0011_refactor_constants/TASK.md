# 任务 0011：魔法数字提成常量

`shipping.py` 里散落着 `800`、`5.0`、`0.13` 三个魔法数字。

要求：行为完全不变，把它们提成模块级常量 `FREE_SHIPPING_THRESHOLD`、
`BASE_FEE`、`TAX_RATE`。

`test_shipping.py` 必须保持全绿；`test_contract.py` 会检查常量存在且取值不变。

约束：
- 只能改源码（`shipping.py`），不能改测试文件；
- 改完必须跑一次 `run_tests` 确认；
- 测试全绿后调用 `finish`。
