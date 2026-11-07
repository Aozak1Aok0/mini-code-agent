# mini-code-agent

沙箱里的 coding agent MVP：读代码 → 改文件 → 跑测试 → 失败后自我修复。

定位是「小任务 + 强评测」，不是通用编程助手：每个任务是一个带 `pytest` 的小仓库，
agent 在独立 workspace 里把测试跑绿，评测看解决率、步数、token 与失败分类。

- 评测页（数字与逐题 trace）：https://aozak1aok0.github.io/mini-code-agent/
- 完整报告：[docs/report.md](docs/report.md)

## 快速开始

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m codeagent.run --task tasks/0001_mean_empty
```

跑完会在 `runs/<task>-<时间>/` 留下 `workspace/`（agent 改过的仓库）和 `result.json`（逐步 trace）。

## 结构

```
codeagent/
  loop.py         agent 循环：模型 → 工具 → 观察，直到 finish 或步数上限
  tools.py        6 个工具：list_dir / read_file / grep / write_file / run_tests / finish
  sandbox.py      workspace 路径白名单 + 受限 pytest 子进程
  credentials.py  Windows 凭据管理器读 key（不落盘）
  run.py          CLI：复制任务 → 跑 agent → 落盘结果
tasks/            任务仓库快照（每个目录一份带失败测试的小项目）
```

## 沙箱边界

MVP 的隔离：

- 文件操作只能落在 workspace 根目录内（拒绝绝对路径与 `..`）；
- 只允许跑 `pytest`，带超时；环境变量最小化；
- 不提供网络工具，agent 无法外联。

这是 Windows 上「真隔离」的合理替代。要更强隔离（Docker / nsjail / 只读挂载）见后续加固。

## 评测

21 个任务（10 bugfix / 4 feature / 4 refactor / 2 perf / 1 long），每个任务是一个带失败 `pytest` 的小仓库；其中 0013–0015 只给现象、不给文件名，需要先复现再定位：

```powershell
.\.venv\Scripts\python.exe -m evals.run_suite              # 全量
.\.venv\Scripts\python.exe -m evals.run_suite --list        # 只列任务，不调用模型
```

评测脚本自己跑 pytest 验收，并校验 `test_*.py` 的哈希——测试被改过就不算通过，
防止 agent 靠弱化测试拿分。21 个任务都带 `hidden/test_hidden.py`：复制时排除、可见测试通过后
再跑一遍，失败记 `hidden_test_failed`。结果落在 `runs/suite-<时间>/results.jsonl` 与 `summary.md`。

基线（2026-11-05，单次全量，`deepseek-chat`）：

| 指标 | 值 |
|---|---|
| 解决率 | 21 / 21（100%） |
| 平均步数 | 9.7 |
| token / 任务 | 14,069 in / 715 out |
| 延迟 P50 | 7.2s |
| 测试被改动 | 0 / 21 |

失败分类：定位错（`no_edit`）、改错（`wrong_fix`）、没跑测试（`no_test_run`）、
循环（`loop`）、改了测试（`tests_modified`）、调用异常（`error`）。

**这条基线没有区分度**：20/20 说明题目对当前模型太简单，失败分类器还拿不到样本。
加难度后的对比：3 个隐式需求任务（只说现象、跨文件定位）步数 9.0 vs 7.5、输入 token +21%，
仍然全绿。隐藏测试两次抓到问题：0005（TASK.md 只写 CRLF、测试要求裸 CR，属超纲）与 0016（可见绿、
原子性没做，属半吊子修复）；前者补 spec、后者补 spec 后也过。0018（多文件重构 + 公共 API 约束）同样 14 步、21,864 in 通过——只要放在题面里，模型能读出「两个版本舍入不同」这种约束。0019（性能热点）更直接：可见测试就把 7 秒的耗时摆在那，模型加个 id 索引就收工。0020 把线索藏进题面（可见全绿、性能只在隐藏测试），模型自己写了 `bench_tmp.py` 造基准再优化——19 步、41k 输入，成本最高，但仍然全绿。

分析见 [`evals/reports/w2-baseline.md`](evals/reports/w2-baseline.md) 与
[`evals/reports/w3-difficulty.md`](evals/reports/w3-difficulty.md)。五个大题（0016–0020）步数 14.2 vs 7.5、输入 token 2.9 倍，解决率仍 100%——
这套题现在测的是成本，不是成功率。下一步方向：写不清楚也得做对的要求（性能预算、兼容旧数据、跨模块不变量）、
模糊需求，或错误点离症状 4 层以上的仓库。
