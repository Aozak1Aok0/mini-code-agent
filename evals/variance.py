"""重复跑同一批题，看成功率和成本的方差。

用法：
    .\\.venv\\Scripts\\python.exe -m evals.variance --reps 3
    .\\.venv\\Scripts\\python.exe -m evals.variance --reps 3 --tasks "tasks/001[6-9]_*,tasks/002[01]_*"
"""

import argparse
import json
import statistics
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BIG = "tasks/001[6-9]_*,tasks/002[01]_*"


def run_rep(rep: int, tasks: str, max_rounds: int) -> Path:
    out = ROOT / "runs" / f"var-rep{rep}"
    if out.exists():
        for child in out.iterdir():
            if child.is_dir():
                import shutil

                shutil.rmtree(child)
    subprocess.run(
        [
            sys.executable,
            "-m",
            "evals.run_suite",
            "--tasks",
            tasks,
            "--max-steps",
            str(max_rounds),
            "--out-dir",
            str(out),
        ],
        cwd=str(ROOT),
        check=True,
        stdout=subprocess.DEVNULL,
    )
    return out


def load(out: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in (out / "results.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--tasks", default=BIG)
    ap.add_argument("--max-rounds", "--max-steps", dest="max_rounds", type=int, default=40)
    args = ap.parse_args()

    runs = []
    for rep in range(1, args.reps + 1):
        print(f"[rep {rep}/{args.reps}]", flush=True)
        runs.append(load(run_rep(rep, args.tasks, args.max_rounds)))

    tasks = sorted({r["task"] for rows in runs for r in rows})
    lines = ["# 重复运行方差", "", f"- 轮数：{args.reps}", f"- 任务：{len(tasks)}", ""]
    lines.append("| 任务 | 解决 | 步数 | 轮数 | 输入 token | 耗时 |")
    lines.append("|---|---|---|---|---|---|")

    total_steps, total_in, solved_all = [], [], 0
    for task in tasks:
        rows = [r for run in runs for r in run if r["task"] == task]
        solved = sum(1 for r in rows if r["solved"])
        solved_all += solved
        steps = [r["steps"] for r in rows]
        rounds = [r["rounds"] for r in rows]
        tin = [r["tokens_in"] for r in rows]
        ms = [r["elapsed_ms"] for r in rows]
        total_steps += steps
        total_in += tin
        sd = statistics.stdev(steps) if len(steps) > 1 else 0.0
        lines.append(
            f"| {task} | {solved}/{len(rows)} | {min(steps)}–{max(steps)} | {min(rounds)}–{max(rounds)} | "
            f"{round(statistics.mean(tin)):,} | {round(statistics.mean(ms) / 1000, 1)}s |"
        )

    n = len(tasks) * args.reps
    lines += [
        "",
        f"合计：{solved_all}/{n} 解决；平均 {statistics.mean(total_steps):.1f} 步、"
        f"{round(statistics.mean(total_in)):,} 输入 token。",
        "",
    ]
    md = ROOT / "runs" / "variance.md"
    md.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    print(f"写入 {md}")


if __name__ == "__main__":
    main()
