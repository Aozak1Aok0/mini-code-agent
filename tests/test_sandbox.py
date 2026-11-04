"""沙箱边界与工具行为的单元测试（不调用模型，CI 可跑）。"""

import pytest

from codeagent.sandbox import SandboxError, Workspace
from codeagent import tools


def test_jail_blocks_parent_escape(tmp_path):
    ws = Workspace(tmp_path / "workspace")
    with pytest.raises(SandboxError):
        ws.resolve("../outside.txt")


def test_jail_blocks_absolute_path(tmp_path):
    ws = Workspace(tmp_path / "workspace")
    with pytest.raises(SandboxError):
        ws.resolve(str(tmp_path / "outside.txt"))


def test_write_read_roundtrip(tmp_path):
    ws = Workspace(tmp_path / "workspace")
    assert tools.write_file(ws, "pkg/mod.py", "x = 1\n")["ok"]
    out = tools.read_file(ws, "pkg/mod.py")
    assert "x = 1" in out["content"]


def test_run_tests_reports_failure_then_pass(tmp_path):
    ws = Workspace(tmp_path / "workspace")
    (ws.root / "test_demo.py").write_text(
        "from demo import add\n\ndef test_add():\n    assert add(1, 2) == 3\n", encoding="utf-8"
    )
    (ws.root / "demo.py").write_text("def add(a, b):\n    return a - b\n", encoding="utf-8")
    assert ws.run_tests()["passed"] is False

    tools.write_file(ws, "demo.py", "def add(a, b):\n    return a + b\n")
    assert ws.run_tests()["passed"] is True
