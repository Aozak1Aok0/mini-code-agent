# W2 任务集基线（12 题，2026-11-05）

12 个任务：5 bugfix / 4 feature / 3 refactor，每个任务是一个带失败 `pytest` 的小仓库。
单次全量运行，`deepseek-chat`，`max_steps=12`，`temperature=0`。

## 结果

| 指标 | 值 |
|---|---|
| 解决率 | 12 / 12（100%） |
| 平均步数 | 7.2 |
| token / 任务 | 输入 8,029、输出 454 |
| 延迟 P50 | 6.9s |
| 测试被改动 | 0 / 12 |

| 任务 | 类别 | 步数 | token(in/out) | 延迟 |
|---|---|---|---|---|
| 0001_mean_empty | bugfix | 7 | 7308/380 | 6901ms |
| 0002_bugfix_chunk | bugfix | 6 | 6917/361 | 6399ms |
| 0003_bugfix_slug | bugfix | 6 | 6346/315 | 5594ms |
| 0004_bugfix_default | bugfix | 7 | 8095/298 | 7149ms |
| 0005_bugfix_crlf | bugfix | 7 | 8343/350 | 6956ms |
| 0006_feature_duration | feature | 7 | 8115/569 | 7750ms |
| 0007_feature_retry | feature | 7 | 8250/494 | 6479ms |
| 0008_feature_paginate | feature | 7 | 8460/585 | 8398ms |
| 0009_feature_csv | feature | 7 | 7433/420 | 7100ms |
| 0010_refactor_validate | refactor | 8 | 9222/478 | 6406ms |
| 0011_refactor_constants | refactor | 9 | 8204/577 | 6736ms |
| 0012_refactor_split | refactor | 8 | 9656/617 | 6999ms |

## 这条基线说明了什么

1. **题目太简单。** 12/12 没有区分度，失败分类器一个样本都没拿到。当前这组数字只能证明
   「harness 能跑、循环稳定、不会死循环」，不能证明 agent 的代码能力。
2. **步数分布很窄（6–9 步）。** 每个任务都是「列目录 → 读源码 → 读测试 → 改 → 跑 → 绿」，
   没有出现需要回退、试错、多次定位的任务。这是难度不足的直接证据，不是 agent 强。
3. **没有靠改测试通过。** 12 个 workspace 的 `test_*.py` 哈希与原始任务一致；评测脚本在
   agent 跑完后自己再跑一次 pytest，并单独校验测试文件指纹。
4. **成本很低。** 全量一轮输入 96,349 token、输出 5,444 token，约 $0.03。这让「每个 commit
   都跑一遍全量任务集」在成本上可行。

## 下一步（W3）

- 加区分度：多文件改动、隐式需求（只说现象不说位置）、需要先复现再修、性能/超时类任务；
- 失败分类目前只有定义没有样本，W3 要让它真的能区分「定位错 / 改错 / 没跑测试 / 循环」；
- 判分只看 pytest 全绿，不看 diff 是否最小；可加「改动行数 / 是否动了无关文件」作为辅助指标。

## 复现

```powershell
.\.venv\Scripts\python.exe -m evals.run_suite
# 或只跑一部分
.\.venv\Scripts\python.exe -m evals.run_suite --tasks "tasks/0006_*"
```

产物在 `runs/suite-<时间>/`：`results.jsonl`（逐题记录）、`summary.md`（汇总表）。
