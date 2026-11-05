"""批量跑任务集：每个任务复制到独立 workspace，agent 修完后由评测脚本自己跑 pytest 验收。

用法：
  python -m evals.run_suite                 # 跑 tasks/0* 全部
  python -m evals.run_suite --limit 3       # 只跑前 3 个
  python -m evals.run_suite --tasks "tasks/0006_*" --max-steps 10
  python -m evals.run_suite --list          # 只列任务，不调用模型

产物：runs/suite-<时间>/results.jsonl 与 summary.md（含解决率、步数、token、P50 延迟、失败分类）。
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import statistics
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

from codeagent.loop import Agent
from codeagent.sandbox import Workspace

ROOT = Path(__file__).resolve().parent.parent
TEST_TIMEOUT = 120


def find_tasks(pattern: str) -> list[Path]:
    return sorted(p for p in ROOT.glob(pattern) if p.is_dir() and (p / "TASK.md").exists())


CATEGORIES = {"0001_mean_empty": "bugfix"}


def category_of(task_dir: Path) -> str:
    name = task_dir.name
    if name in CATEGORIES:
        return CATEGORIES[name]
    for cat in ("bugfix", "feature", "refactor"):
        if cat in name:
            return cat
    return "unknown"


def test_hashes(task_dir: Path) -> dict[str, str]:
    """测试文件的指纹：跑之前和跑之后必须一致，否则结果不算数。"""
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(task_dir.glob("test_*.py"))}


def verify(workspace: Path) -> tuple[bool, str]:
    """评测脚本自己跑一次 pytest，不依赖 agent 的 run_tests 结论。"""
    try:
        out = subprocess.run(
            [sys.executable, "-m", "pytest", "-q"],
            cwd=str(workspace),
            capture_output=True,
            text=True,
            timeout=TEST_TIMEOUT,
        )
        return out.returncode == 0, (out.stdout + out.stderr).strip()
    except subprocess.TimeoutExpired:
        return False, f"pytest 超时（>{TEST_TIMEOUT}s）"


def classify(result, solved: bool, max_steps: int) -> str:
    if result is not None and result.error:
        return "error"
    if solved:
        tools = [s.tool for s in result.steps] if result else []
        return "solved_without_tests" if "run_tests" not in tools else "solved"
    if result is None:
        return "error"
    if not result.finished and len(result.steps) >= max_steps:
        return "loop"
    tools = [s.tool for s in result.steps]
    if "write_file" not in tools:
        return "no_edit"
    if "run_tests" not in tools:
        return "no_test_run"
    return "wrong_fix"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks", default="tasks/0*", help="glob，默认 tasks/0*")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--max-steps", type=int, default=12)
    ap.add_argument("--model", default="deepseek-chat")
    ap.add_argument("--out-dir", default="")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    tasks = find_tasks(args.tasks)
    if args.limit:
        tasks = tasks[: args.limit]
    if not tasks:
        raise SystemExit(f"没有匹配 {args.tasks} 的任务目录")
    if args.list:
        for t in tasks:
            print(f"{t.name:<26} {category_of(t)}")
        return

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = Path(args.out_dir) if args.out_dir else ROOT / "runs" / f"suite-{stamp}"
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"任务数：{len(tasks)} · 输出：{out_dir}\n")

    records = []
    for task_dir in tasks:
        ws = out_dir / task_dir.name / "workspace"
        shutil.copytree(task_dir, ws)
        prompt = (task_dir / "TASK.md").read_text(encoding="utf-8")
        hashes_before = test_hashes(task_dir)

        started = time.monotonic()
        result = None
        try:
            agent = Agent(Workspace(ws), model=args.model, max_steps=args.max_steps)
            result = agent.run(prompt)
        except Exception as e:  # noqa: BLE001
            err = f"{type(e).__name__}: {e}"
        else:
            err = ""
        elapsed_ms = int((time.monotonic() - started) * 1000)

        solved, pytest_out = verify(ws)
        tests_modified = test_hashes(ws) != hashes_before
        if tests_modified:
            solved = False
            failure = "tests_modified"
        else:
            failure = classify(result, solved, args.max_steps)

        rec = {
            "task": task_dir.name,
            "category": category_of(task_dir),
            "solved": solved,
            "failure": failure,
            "tests_modified": tests_modified,
            "finished": bool(result and result.finished),
            "steps": len(result.steps) if result else 0,
            "tokens_in": result.tokens_in if result else 0,
            "tokens_out": result.tokens_out if result else 0,
            "elapsed_ms": elapsed_ms,
            "error": err or (result.error if result else ""),
            "pytest_tail": "\n".join(pytest_out.splitlines()[-6:]),
            "steps_trace": [{"tool": s.tool, "ok": s.ok} for s in result.steps] if result else [],
        }
        records.append(rec)
        print(f"{task_dir.name:<26} {'PASS' if solved else 'FAIL':<5} {failure:<20} "
              f"steps={rec['steps']:<2} token={rec['tokens_in']}/{rec['tokens_out']} {elapsed_ms}ms")

    (out_dir / "results.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in records) + "\n", encoding="utf-8"
    )

    solved = sum(r["solved"] for r in records)
    lat = [r["elapsed_ms"] for r in records]
    by_cat: dict[str, list[bool]] = {}
    for r in records:
        by_cat.setdefault(r["category"], []).append(r["solved"])

    lines = [
        f"# 任务集结果（{stamp}）",
        "",
        f"- 解决率：{solved}/{len(records)} = {solved / len(records):.1%}",
        f"- 平均步数：{statistics.mean(r['steps'] for r in records):.1f}",
        f"- token/任务：输入 {statistics.mean(r['tokens_in'] for r in records):.0f}、"
        f"输出 {statistics.mean(r['tokens_out'] for r in records):.0f}",
        f"- 延迟 P50：{statistics.median(lat):.0f}ms",
        "",
        "| 任务 | 类别 | 结果 | 失败分类 | 步数 | token(in/out) | 延迟 |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in records:
        lines.append(
            f"| {r['task']} | {r['category']} | {'✅' if r['solved'] else '❌'} | {r['failure']} | "
            f"{r['steps']} | {r['tokens_in']}/{r['tokens_out']} | {r['elapsed_ms']}ms |"
        )
    lines += ["", "## 分类", ""]
    for cat, vals in sorted(by_cat.items()):
        lines.append(f"- {cat}: {sum(vals)}/{len(vals)}")
    lines += ["", "## 失败分类", ""]
    fails: dict[str, int] = {}
    for r in records:
        if not r["solved"]:
            fails[r["failure"]] = fails.get(r["failure"], 0) + 1
    for k, v in sorted(fails.items()):
        lines.append(f"- {k}: {v}")
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\n解决率 {solved}/{len(records)} · 汇总：{out_dir / 'summary.md'}")


if __name__ == "__main__":
    main()
