# 任务 0004：默认值没生效

`pytest -q` 会失败：`get_setting()` 声明了 `default` 参数却没使用，
配置里没有该 key 时直接抛 `KeyError`。

约束：
- 只能改源码（`settings.py`），不能改 `test_settings.py`；
- 改完必须跑一次 `run_tests` 确认；
- 测试全绿后调用 `finish`。
