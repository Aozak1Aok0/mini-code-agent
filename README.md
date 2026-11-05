# mini-code-agent

沙箱里的 coding agent MVP：读代码 → 改文件 → 跑测试 → 失败后自我修复。

定位是「小任务 + 强评测」，不是通用编程助手：每个任务是一个带 `pytest` 的小仓库，
agent 在独立 workspace 里把测试跑绿，评测看解决率、步数、token 与失败分类。

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

12 个任务（5 bugfix / 4 feature / 3 refactor），每个任务是一个带失败 `pytest` 的小仓库：

```powershell
.\.venv\Scripts\python.exe -m evals.run_suite              # 全量
.\.venv\Scripts\python.exe -m evals.run_suite --list        # 只列任务，不调用模型
```

评测脚本自己跑 pytest 验收，并校验 `test_*.py` 的哈希——测试被改过就不算通过，
防止 agent 靠弱化测试拿分。结果落在 `runs/suite-<时间>/results.jsonl` 与 `summary.md`。

基线（2026-11-05，单次全量，`deepseek-chat`）：

| 指标 | 值 |
|---|---|
| 解决率 | 12 / 12（100%） |
| 平均步数 | 7.2 |
| token / 任务 | 8,029 in / 454 out |
| 延迟 P50 | 6.9s |
| 测试被改动 | 0 / 12 |

失败分类：定位错（`no_edit`）、改错（`wrong_fix`）、没跑测试（`no_test_run`）、
循环（`loop`）、改了测试（`tests_modified`）、调用异常（`error`）。

**这条基线没有区分度**：12/12 说明题目对当前模型太简单，失败分类器还拿不到样本。
分析见 [`evals/reports/w2-baseline.md`](evals/reports/w2-baseline.md)；W3 加难度（多文件、
隐式需求、先复现再修、性能类）后再看这组指标的变化。
