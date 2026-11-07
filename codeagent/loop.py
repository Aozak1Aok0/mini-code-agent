"""最小可用的 coding agent 循环：模型 → 工具 → 观察 → 继续，直到 finish 或步数上限。"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field

from openai import OpenAI

from . import tools
from .credentials import get_deepseek_key
from .sandbox import Workspace

SYSTEM = """你是一个在隔离工作区里干活的 coding agent。
目标：让仓库里的测试全部通过。

规则：
1. 先看：list_dir / read_file / grep 定位失败原因，不要一上来就改。
2. 一次只改一处；write_file 必须写完整文件，不是 diff。
3. 每次改完立刻 run_tests，根据报错继续。
4. 测试全绿后调用 finish，一句话总结改了什么。
5. 不许改测试文件，不许操作 workspace 之外的东西。"""


@dataclass
class Step:
    n: int
    tool: str
    args: dict
    ok: bool
    output: str
    ms: int


@dataclass
class Result:
    finished: bool
    passed: bool
    summary: str
    steps: list[Step] = field(default_factory=list)
    rounds: int = 0
    tokens_in: int = 0
    tokens_out: int = 0
    error: str = ""


class Agent:
    def __init__(
        self,
        workspace: Workspace,
        *,
        model: str = "deepseek-chat",
        max_rounds: int = 12,
        client: OpenAI | None = None,
    ) -> None:
        self.ws = workspace
        self.model = model
        self.max_rounds = max_rounds
        self.client = client or OpenAI(api_key=get_deepseek_key(), base_url="https://api.deepseek.com")

    def run(self, task: str) -> Result:
        messages: list[dict] = [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": task},
        ]
        result = Result(finished=False, passed=False, summary="")

        for round_no in range(1, self.max_rounds + 1):
            result.rounds = round_no
            try:
                resp = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    tools=tools.SCHEMAS,
                    tool_choice="auto",
                    temperature=0,
                )
            except Exception as e:  # noqa: BLE001
                result.error = f"LLM 调用失败：{type(e).__name__}: {e}"
                return result

            if resp.usage:
                result.tokens_in += resp.usage.prompt_tokens
                result.tokens_out += resp.usage.completion_tokens

            msg = resp.choices[0].message
            messages.append(msg.model_dump(exclude_none=True))

            if not msg.tool_calls:
                # 模型没调工具：当作一次面向人的回答，但任务未完成，继续催
                messages.append({"role": "user", "content": "请继续用工具推进任务；完成后调用 finish。"})
                continue

            for call in msg.tool_calls:
                t0 = time.perf_counter()
                try:
                    args = json.loads(call.function.arguments or "{}")
                except json.JSONDecodeError:
                    args = {}
                    out = {"ok": False, "error": "参数不是合法 JSON"}
                else:
                    out = tools.call(self.ws, call.function.name, args)
                ms = int((time.perf_counter() - t0) * 1000)

                result.steps.append(
                    Step(
                        n=round_no,
                        tool=call.function.name,
                        args=args,
                        ok=bool(out.get("ok")),
                        output=str(out.get("content") or out.get("error") or "")[:1500],
                        ms=ms,
                    )
                )
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": call.id,
                        "content": json.dumps(out, ensure_ascii=False),
                    }
                )

                if out.get("finished"):
                    result.finished = True
                    result.summary = out.get("summary", "")
                    tests = self.ws.run_tests()
                    result.passed = tests["passed"]
                    return result

        result.summary = "达到轮数上限"
        result.passed = self.ws.run_tests()["passed"]
        return result
