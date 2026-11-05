# 0018 结算逻辑去重（重构 + 公共 API 约束）

## 背景

`orders_a.py` 和 `orders_b.py` 各有一份结算实现，是历史上两次迁移留下的。

- `orders_a.total(items)`：总价 `.5` 一律**进位**（2.5 → 3）。
- `orders_b.total(items)`：总价 `.5` **取偶**（2.5 → 2，3.5 → 4）。

两份实现在 `.5` 的边界上行为不同，这是业务现状，两个调用方都依赖它。

## 任务

把求和与取整的逻辑抽到新模块 `pricing.py`，让 `orders_a` / `orders_b` 变成薄封装：

- `pricing.sum_items(items) -> float`：只求和，不做任何取整。
- `pricing.total(items, mode) -> int`：`mode` 为 `"half_up"` 时 `.5` 进位，为 `"banker"` 时 `.5` 取偶；其它值抛 `ValueError`。
- `orders_a.total(items)` 与 `orders_b.total(items)` 的返回值和现在**完全一致**，签名不变。
- `api.quote` / `api.both` 的行为不变。

## 验收

- `pytest` 全绿。
- 原有可见测试不能改（`test_orders.py` 的断言保持原样）。
- 两个旧模块仍然可以单独 import 并调用。
