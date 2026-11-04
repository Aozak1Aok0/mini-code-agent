"""Agent 的工具层：读代码、写文件、跑测试。

所有文件路径都经过 Workspace.resolve，越界直接抛 SandboxError（工具会把它转成错误结果，
让模型自己看到并纠正）。
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from .sandbox import SandboxError, Workspace

SKIP_DIRS = {".git", ".venv", "__pycache__", "node_modules", ".pytest_cache", "runs"}
MAX_OUTPUT = 4000


def _clip(text: str, limit: int = MAX_OUTPUT) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + f"\n...（截断，共 {len(text)} 字符）"


def list_dir(ws: Workspace, path: str = ".") -> dict:
    target = ws.resolve(path)
    if not target.is_dir():
        return {"ok": False, "error": f"不是目录：{path}"}
    rows = []
    for p in sorted(target.iterdir()):
        if p.name in SKIP_DIRS:
            continue
        rows.append(f"{p.name}/" if p.is_dir() else f"{p.name}  ({p.stat().st_size}B)")
    return {"ok": True, "content": _clip("\n".join(rows) or "（空目录）")}


def read_file(ws: Workspace, path: str, offset: int = 0, limit: int = 400) -> dict:
    target = ws.resolve(path)
    if not target.is_file():
        return {"ok": False, "error": f"不是文件：{path}"}
    if target.stat().st_size > 400_000:
        return {"ok": False, "error": "文件过大（>400KB），请用 grep 定位"}
    lines = target.read_text(encoding="utf-8", errors="replace").splitlines()
    chunk = lines[offset : offset + limit]
    body = "\n".join(f"{i + offset + 1:>4}| {line}" for i, line in enumerate(chunk))
    tail = "" if offset + limit >= len(lines) else f"\n...（还有 {len(lines) - offset - limit} 行）"
    return {"ok": True, "content": _clip(body + tail), "lines": len(lines)}


def grep(ws: Workspace, pattern: str, glob: str = "**/*", limit: int = 40) -> dict:
    try:
        rx = re.compile(pattern)
    except re.error as e:
        return {"ok": False, "error": f"正则不合法：{e}"}
    hits = []
    for p in ws.root.glob(glob):
        if not p.is_file() or any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.suffix.lower() in {".png", ".jpg", ".zip", ".onnx", ".db"}:
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for no, line in enumerate(text.splitlines(), 1):
            if rx.search(line):
                rel = p.relative_to(ws.root).as_posix()
                hits.append(f"{rel}:{no}: {line.strip()[:200]}")
                if len(hits) >= limit:
                    return {"ok": True, "content": _clip("\n".join(hits))}
    return {"ok": True, "content": _clip("\n".join(hits) or "（无匹配）")}


def write_file(ws: Workspace, path: str, content: str) -> dict:
    target = ws.resolve(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    before = target.read_text(encoding="utf-8", errors="replace") if target.exists() else ""
    target.write_text(content, encoding="utf-8", newline="\n")
    return {
        "ok": True,
        "content": f"已写入 {path}（{len(before.splitlines())} → {len(content.splitlines())} 行）",
    }


def run_tests(ws: Workspace, timeout: int = 120) -> dict:
    result = ws.run_tests(timeout=timeout)
    return {"ok": True, "content": _clip(json.dumps(result, ensure_ascii=False, indent=1)), "passed": result["passed"]}


TOOLS = {
    "list_dir": list_dir,
    "read_file": read_file,
    "grep": grep,
    "write_file": write_file,
    "run_tests": run_tests,
}

SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "list_dir",
            "description": "列出目录内容（只读）。",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string", "description": "相对 workspace 的目录，默认 ."}},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "按行读文件，返回带行号的内容（只读）。",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "offset": {"type": "integer", "description": "起始行，0 基，默认 0"},
                    "limit": {"type": "integer", "description": "最多读几行，默认 400"},
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "grep",
            "description": "在 workspace 内按正则搜索代码（只读），返回 文件:行号: 内容。",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {"type": "string"},
                    "glob": {"type": "string", "description": "文件过滤，默认 **/*"},
                    "limit": {"type": "integer", "description": "最多返回条数，默认 40"},
                },
                "required": ["pattern"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "写入（覆盖）整个文件；内容必须是完整文件，不是 diff。",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}, "content": {"type": "string"}},
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_tests",
            "description": "在 workspace 根目录跑 pytest -q，返回退出码与输出。改完代码必须跑一次。",
            "parameters": {
                "type": "object",
                "properties": {"timeout": {"type": "integer", "description": "秒，默认 120"}},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "finish",
            "description": "任务完成且测试全绿后调用；附带一句话总结改了什么。",
            "parameters": {
                "type": "object",
                "properties": {"summary": {"type": "string"}},
                "required": ["summary"],
            },
        },
    },
]


def call(ws: Workspace, name: str, args: dict) -> dict:
    if name == "finish":
        return {"ok": True, "content": "已结束", "finished": True, "summary": args.get("summary", "")}
    fn = TOOLS.get(name)
    if fn is None:
        return {"ok": False, "error": f"未知工具：{name}"}
    try:
        return fn(ws, **args)
    except SandboxError as e:
        return {"ok": False, "error": str(e)}
    except TypeError as e:
        return {"ok": False, "error": f"参数不匹配：{e}"}
