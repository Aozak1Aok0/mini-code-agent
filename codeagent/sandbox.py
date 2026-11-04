"""工作区沙箱：路径白名单 + 受限命令执行。

MVP 的隔离边界：
- 所有文件操作只能落在 workspace 根目录内（防 `..` 与绝对路径）；
- 子进程只跑 pytest，超时 kill，环境变量最小化；
- 不提供网络工具（agent 只能读/写/跑测试）。

这是 Windows 上「真隔离」的合理替代；要更强的隔离（Docker/nsjail）见 README 的加固项。
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


class SandboxError(RuntimeError):
    """越界或不允许的操作。"""


class Workspace:
    def __init__(self, root: Path) -> None:
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def resolve(self, rel: str) -> Path:
        if rel in ("", ".", "./"):
            return self.root
        p = Path(rel)
        if p.is_absolute():
            raise SandboxError(f"不允许绝对路径：{rel}")
        target = (self.root / p).resolve()
        if target != self.root and not target.is_relative_to(self.root):
            raise SandboxError(f"越界路径：{rel}")
        return target

    def run_tests(self, timeout: int = 120) -> dict:
        env = {
            "PATH": os.environ.get("PATH", ""),
            "SYSTEMROOT": os.environ.get("SYSTEMROOT", ""),
            "PYTHONIOENCODING": "utf-8",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
        try:
            cp = subprocess.run(
                [sys.executable, "-m", "pytest", "-q"],
                cwd=self.root,
                capture_output=True,
                text=True,
                timeout=timeout,
                env=env,
            )
        except subprocess.TimeoutExpired:
            return {"exit_code": -1, "passed": False, "output": f"超时（>{timeout}s），进程已终止"}
        output = ((cp.stdout or "") + (cp.stderr or "")).strip()
        return {"exit_code": cp.returncode, "passed": cp.returncode == 0, "output": output[-4000:]}
