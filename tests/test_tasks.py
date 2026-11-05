"""任务夹具的守门测试：每个任务目录必须是「带 TASK.md、带测试、初始为红」的完整小仓库。

不调用模型，CI 里几秒钟跑完。任何任务被改坏（测试被改绿、源码缺失、TASK.md 丢了）都会在这里暴露。
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS = sorted(p for p in (ROOT / "tasks").iterdir() if p.is_dir())


def test_have_tasks():
    assert len(TASKS) == 12, f"期望 12 个任务，实际 {len(TASKS)}"


def test_each_task_is_well_formed():
    for t in TASKS:
        assert (t / "TASK.md").exists(), f"{t.name} 缺 TASK.md"
        tests = list(t.glob("test_*.py"))
        assert tests, f"{t.name} 没有任何 test_*.py"
        sources = [p for p in t.glob("*.py") if not p.name.startswith("test_")]
        assert sources, f"{t.name} 没有源码文件"


def test_each_task_starts_red():
    for t in TASKS:
        out = subprocess.run(
            [sys.executable, "-m", "pytest", "-q"],
            cwd=str(t),
            capture_output=True,
            text=True,
            timeout=120,
        )
        assert out.returncode != 0, f"{t.name} 初始就是绿的，agent 无活可干"
