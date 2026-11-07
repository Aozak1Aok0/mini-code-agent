"""CLI：把 tasks/<id>/ 复制到 runs/<id>-<时间>/workspace，让 agent 在里面修，最后报告。

用法：
  python -m codeagent.run --task tasks/0001_mean_empty
  python -m codeagent.run --task tasks/0001_mean_empty --max-steps 8 --keep
"""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path

from .loop import Agent
from .sandbox import Workspace

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True, help="任务目录（包含仓库文件与 test_*.py）")
    ap.add_argument("--runs-dir", default=str(ROOT / "runs"))
    ap.add_argument("--max-rounds", type=int, default=12)
    ap.add_argument("--model", default="deepseek-chat")
    ap.add_argument("--keep", action="store_true", help="保留 workspace（默认保留）")
    args = ap.parse_args()

    task_dir = Path(args.task)
    if not task_dir.is_dir():
        raise SystemExit(f"任务目录不存在：{task_dir}")

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = Path(args.runs_dir) / f"{task_dir.name}-{stamp}"
    ws_dir = run_dir / "workspace"
    shutil.copytree(task_dir, ws_dir)

    prompt = (task_dir / "TASK.md").read_text(encoding="utf-8") if (task_dir / "TASK.md").exists() else (
        "仓库里有测试失败。请定位并修复源码，让 pytest 全部通过；不要修改测试文件。"
    )

    print(f"任务：{task_dir.name}\n工作区：{ws_dir}\n")
    agent = Agent(Workspace(ws_dir), model=args.model, max_rounds=args.max_rounds)
    result = agent.run(prompt)

    for s in result.steps:
        print(f"[{s.n:>2}] {s.tool:<10} {'ok ' if s.ok else 'ERR'} {s.ms:>5}ms  {s.output.splitlines()[0][:90] if s.output else ''}")
    print("-" * 70)
    print(f"完成：{result.finished} · 测试通过：{result.passed} · 步数：{len(result.steps)} · "
          f"token：{result.tokens_in}/{result.tokens_out}")
    if result.summary:
        print(f"总结：{result.summary}")
    if result.error:
        print(f"错误：{result.error}")

    (run_dir / "result.json").write_text(
        json.dumps(
            {
                "task": task_dir.name,
                "finished": result.finished,
                "passed": result.passed,
                "summary": result.summary,
                "tokens_in": result.tokens_in,
                "tokens_out": result.tokens_out,
                "error": result.error,
                "steps": [vars(s) for s in result.steps],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"结果：{run_dir / 'result.json'}")


if __name__ == "__main__":
    main()
