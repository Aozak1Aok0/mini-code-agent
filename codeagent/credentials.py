"""从 Windows 凭据管理器读 DeepSeek key（不落盘），环境变量优先。"""

from __future__ import annotations

import ctypes
import os
from ctypes import wintypes

DEFAULT_TARGET = "WorkBuddy/DeepSeek"
CRED_TYPE_GENERIC = 1


class _CREDENTIAL(ctypes.Structure):
    _fields_ = [
        ("Flags", wintypes.DWORD),
        ("Type", wintypes.DWORD),
        ("TargetName", wintypes.LPWSTR),
        ("Comment", wintypes.LPWSTR),
        ("LastWritten", wintypes.FILETIME),
        ("CredentialBlobSize", wintypes.DWORD),
        ("CredentialBlob", ctypes.POINTER(ctypes.c_byte)),
        ("Persist", wintypes.DWORD),
        ("AttributeCount", wintypes.DWORD),
        ("Attributes", ctypes.c_void_p),
        ("TargetAlias", wintypes.LPWSTR),
        ("UserName", wintypes.LPWSTR),
    ]


def _read_windows_cred(target: str) -> str | None:
    advapi32 = ctypes.windll.advapi32
    ptr = ctypes.POINTER(_CREDENTIAL)()
    ok = advapi32.CredReadW(target, CRED_TYPE_GENERIC, 0, ctypes.byref(ptr))
    if not ok:
        return None
    try:
        size = ptr.contents.CredentialBlobSize
        raw = ctypes.string_at(ptr.contents.CredentialBlob, size)
        # Windows 凭据 blob 通常是 UTF-16LE（带 NUL），先按此解码，再退回 UTF-8
        text = raw.decode("utf-16-le", errors="ignore") if b"\x00" in raw else raw.decode("utf-8", errors="ignore")
        return text.strip().strip("\x00") or None
    finally:
        advapi32.CredFree(ptr)


def get_deepseek_key() -> str:
    key = os.getenv("DEEPSEEK_API_KEY")
    if key:
        return key.strip()
    key = _read_windows_cred(os.getenv("CRED_TARGET", DEFAULT_TARGET))
    if not key:
        raise SystemExit(
            "未找到 DeepSeek key：设置 DEEPSEEK_API_KEY，或在凭据管理器创建通用凭据 WorkBuddy/DeepSeek"
        )
    return key
