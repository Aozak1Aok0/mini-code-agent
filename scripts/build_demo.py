# -*- coding: utf-8 -*-
"""从最近一次全量评测结果生成静态 demo 页（docs/index.html）。

用法：
    python scripts/build_demo.py                # 取 runs/ 里最新的 summary.md
    python scripts/build_demo.py --run runs/suite-20261106-130812
"""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO_URL = "https://github.com/Aozak1Aok0/mini-code-agent"


def latest_run() -> Path:
    runs = sorted((ROOT / "runs").glob("suite-*"), key=lambda p: p.stat().st_mtime)
    if not runs:
        raise SystemExit("runs/ 下没有 suite-* 结果，先跑一次 evals.run_suite")
    return runs[-1]


def load_rows(run: Path) -> list[dict]:
    path = run / "results.jsonl"
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return rows


def avg(xs: list[float]) -> float:
    return sum(xs) / len(xs) if xs else 0.0


def fmt_int(n: float) -> str:
    return f"{int(round(n)):,}"


def tool_class(name: str) -> str:
    return {
        "read_file": "read",
        "list_dir": "read",
        "grep": "read",
        "write_file": "write",
        "run_tests": "test",
        "finish": "done",
    }.get(name, "read")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", type=Path, default=None)
    args = ap.parse_args()

    run = args.run or latest_run()
    rows = load_rows(run)
    rows.sort(key=lambda r: r["task"])

    solved = sum(1 for r in rows if r["solved"])
    total = len(rows)
    steps = avg([r["steps"] for r in rows])
    tin = avg([r["tokens_in"] for r in rows])
    tout = avg([r["tokens_out"] for r in rows])
    lat = sorted(r["elapsed_ms"] for r in rows)
    p50 = lat[len(lat) // 2]
    hidden_used = sum(1 for r in rows if r.get("hidden_used"))
    hidden_failed = sum(1 for r in rows if r.get("hidden_failed"))
    touched = sum(1 for r in rows if r.get("tests_modified"))
    max_tin = max(r["tokens_in"] for r in rows)

    cats: dict[str, list[int]] = {}
    for r in rows:
        c = r.get("category") or "unknown"
        cats.setdefault(c, [0, 0])
        cats[c][0] += 1
        cats[c][1] += 1 if r["solved"] else 0

    table_rows = []
    for r in rows:
        chips = "".join(
            f'<span class="chip {tool_class(s["tool"])}" title="{html.escape(s["tool"])}">'
            f'{html.escape(s["tool"].replace("_", " "))}</span>'
            for s in r.get("steps_trace") or []
        )
        table_rows.append(
            "<tr>"
            f'<td class="tid">{html.escape(r["task"])}</td>'
            f'<td><span class="cat cat-{html.escape(r.get("category") or "unknown")}">'
            f'{html.escape(r.get("category") or "unknown")}</span></td>'
            f'<td class="num">{r["steps"]}</td>'
            f'<td class="num">{fmt_int(r["tokens_in"])}</td>'
            f'<td class="num">{r["elapsed_ms"] / 1000:.1f}s</td>'
            f'<td class="tools">{chips}</td>'
            f'<td class="ok">{"✓" if r["solved"] else "✗"}</td>'
            "</tr>"
        )

    bar_rows = []
    for r in rows:
        pct = max(2.0, r["tokens_in"] / max_tin * 100)
        bar_rows.append(
            '<div class="bar-row">'
            f'<span class="bar-label">{html.escape(r["task"][:4])}</span>'
            f'<span class="bar" style="width:{pct:.1f}%"></span>'
            f'<span class="bar-val">{fmt_int(r["tokens_in"])}</span>'
            "</div>"
        )

    cat_line = " · ".join(
        f'{c} {v[1]}/{v[0]}' for c, v in sorted(cats.items())
    )

    page = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>mini-code-agent · 评测报告</title>
<style>
  :root {{ --ink:#1b2330; --muted:#667085; --line:#e4e7ec; --accent:#1f3a5f; --bg:#fbfcfd; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--ink);
         font:15px/1.65 -apple-system,"Segoe UI","Microsoft YaHei",sans-serif; }}
  main {{ max-width:980px; margin:0 auto; padding:56px 24px 80px; }}
  header h1 {{ margin:0 0 6px; font-size:34px; letter-spacing:-.5px; }}
  header p.lead {{ margin:0 0 8px; color:var(--muted); }}
  header .links a {{ color:var(--accent); text-decoration:none; margin-right:16px; font-size:14px; }}
  header .links a:hover {{ text-decoration:underline; }}
  .kpis {{ display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin:32px 0 8px; }}
  .kpi {{ background:#fff; border:1px solid var(--line); border-radius:10px; padding:14px 16px; }}
  .kpi .v {{ font-size:24px; font-weight:650; letter-spacing:-.3px; }}
  .kpi .k {{ font-size:12px; color:var(--muted); margin-top:2px; }}
  h2 {{ font-size:18px; margin:40px 0 12px; padding-bottom:6px; border-bottom:1px solid var(--line); }}
  table {{ width:100%; border-collapse:collapse; background:#fff; font-size:13.5px;
           border:1px solid var(--line); border-radius:10px; overflow:hidden; }}
  th {{ text-align:left; font-weight:600; color:var(--muted); background:#f8fafc;
        padding:9px 10px; border-bottom:1px solid var(--line); font-size:12.5px; }}
  td {{ padding:8px 10px; border-bottom:1px solid #f1f3f6; vertical-align:middle; }}
  tr:last-child td {{ border-bottom:none; }}
  .tid {{ font-family:ui-monospace,Consolas,monospace; font-size:12.5px; }}
  .num {{ text-align:right; font-variant-numeric:tabular-nums; }}
  .ok {{ color:#0f9d58; text-align:center; }}
  .cat {{ font-size:11.5px; padding:1px 7px; border-radius:999px; background:#eef2f7; color:#475467; }}
  .cat-perf {{ background:#fdf2e9; color:#b54708; }}
  .chip {{ display:inline-block; font-size:10.5px; padding:1px 6px; margin:1px 3px 1px 0;
           border-radius:5px; font-family:ui-monospace,Consolas,monospace; }}
  .chip.read {{ background:#eef4ff; color:#3538cd; }}
  .chip.write {{ background:#ecfdf3; color:#067647; }}
  .chip.test {{ background:#fff6ed; color:#b93815; }}
  .chip.done {{ background:#f4f3ff; color:#5925dc; }}
  .bars {{ background:#fff; border:1px solid var(--line); border-radius:10px; padding:16px 18px; }}
  .bar-row {{ display:grid; grid-template-columns:34px 1fr 76px; align-items:center; gap:10px; margin:5px 0; }}
  .bar-label {{ font-family:ui-monospace,Consolas,monospace; font-size:11.5px; color:var(--muted); }}
  .bar {{ display:block; height:12px; background:linear-gradient(90deg,#1f3a5f,#4f7bb5); border-radius:3px; }}
  .bar-val {{ font-size:11.5px; color:var(--muted); text-align:right; font-variant-numeric:tabular-nums; }}
  .note {{ background:#fff; border:1px solid var(--line); border-left:3px solid var(--accent);
           border-radius:8px; padding:14px 18px; margin:14px 0; }}
  .note p {{ margin:6px 0; }}
  ul li {{ margin:5px 0; }}
  footer {{ margin-top:48px; color:var(--muted); font-size:12.5px; }}
  @media (max-width:720px) {{ .kpis {{ grid-template-columns:repeat(2,1fr); }} .tools {{ display:none; }} }}
</style>
</head>
<body>
<main>
  <header>
    <h1>mini-code-agent</h1>
    <p class="lead">沙箱里的 coding agent：读代码 → 改文件 → 跑测试 → 失败后自我修复。</p>
    <p class="lead">评测集 {total} 题 · 单次全量 · deepseek-chat · {html.escape(run.name)}</p>
    <p class="links"><a href="{REPO_URL}">GitHub</a><a href="https://github.com/Aozak1Aok0/mini-code-agent/blob/main/docs/report.md">完整报告</a><a href="{REPO_URL}#快速开始">复现</a></p>
  </header>

  <section class="kpis">
    <div class="kpi"><div class="v">{solved}/{total}</div><div class="k">解决率</div></div>
    <div class="kpi"><div class="v">{steps:.1f}</div><div class="k">平均步数</div></div>
    <div class="kpi"><div class="v">{tin / 1000:.1f}k</div><div class="k">输入 token / 任务</div></div>
    <div class="kpi"><div class="v">{p50 / 1000:.1f}s</div><div class="k">延迟 P50</div></div>
  </section>

  <h2>逐题结果</h2>
  <table>
    <thead><tr><th>任务</th><th>类别</th><th class="num">步数</th><th class="num">输入 token</th>
    <th class="num">耗时</th><th>工具调用序列</th><th>结果</th></tr></thead>
    <tbody>
      {''.join(table_rows)}
    </tbody>
  </table>
  <p class="lead" style="margin-top:10px">分类：{cat_line} · 隐藏测试 {hidden_used}/{total} 启用、{hidden_failed} 失败 · 测试被改动 {touched}/{total}</p>

  <h2>成本曲线</h2>
  <div class="bars">
    {''.join(bar_rows)}
  </div>

  <h2>没做成的事</h2>
  <div class="note">
    <p><strong>指标饱和。</strong> {solved}/{total} 说明题目对当前模型太简单，失败分类器拿不到样本；加难度只抬高成本（大题步数 14.2 vs 7.5、输入 token 2.9 倍），解决率仍是 100%。</p>
    <p><strong>可见信号等于答案。</strong> 0019 把 7 秒的耗时摆在测试里，模型加个索引就收工；0020 把线索藏进题面，模型自己写 <code>bench_tmp.py</code> 造基准再优化——19 步、41k 输入。</p>
    <p><strong>隐藏测试抓的是 spec 缺口，不是能力。</strong> 0005 的 TASK.md 只写 CRLF，测试却要求裸 CR，属超纲；0016 可见绿、原子性没做，属半吊子修复。</p>
  </div>

  <h2>怎么复现</h2>
  <pre style="background:#fff;border:1px solid var(--line);border-radius:8px;padding:14px 16px;overflow:auto;font-size:13px"><code>python -m venv .venv
.\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt
.\\.venv\\Scripts\\python.exe -m evals.run_suite --limit 3   # 先跑 3 题看看
.\\.venv\\Scripts\\python.exe -m evals.run_suite             # 全量 {total} 题</code></pre>

  <footer>
    由 <code>scripts/build_demo.py</code> 从 <code>{html.escape(str(run.relative_to(ROOT)).replace(chr(92), "/"))}/results.jsonl</code> 生成 ·
    平均输出 {tout:.0f} token / 任务
  </footer>
</main>
</body>
</html>
"""
    out = ROOT / "docs" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"saved {out} ({len(page)} chars, {total} tasks)")


if __name__ == "__main__":
    main()


