#!/usr/bin/env python3
"""digest 生成器（消费端 v0）：从基底按时间窗拼装周报。

只读 kb/（基底是唯一事实源）：新入库 items 按 research_line 分组，
高相关优先，带 one_liner / 论断数 / 深读链接。产出 markdown，
后续接 IM/webhook 推送时只换投递方式、不换内容源。

用法：
  uv run --with pyyaml python scripts/make_digest.py                 # 最近 7 天
  uv run --with pyyaml python scripts/make_digest.py --days 30
"""
from __future__ import annotations

import argparse
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ITEMS = ROOT / "kb" / "items" / "papers"
QUEUE = ROOT / "queue" / "papers"
OUT_DIR = ROOT / "docs" / "digests"

LINE_NAMES = {
    "traditional_codec_opt": "传统编码器优化",
    "learned_codec": "学习式编码",
    "coding_for_machines": "面向机器的编码",
    "generative_compression": "生成式压缩",
    "inr_representation": "INR 表示压缩",
    "systems_deployment": "系统与部署",
}
LINE_ORDER = list(LINE_NAMES)


def load(p: Path):
    return yaml.safe_load(open(p, encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=7)
    args = ap.parse_args()

    cutoff = (date.today() - timedelta(days=args.days)).isoformat()
    items = [load(p) for p in sorted(ITEMS.glob("*.yaml"))]

    fresh = [d for d in items if d["time"]["collected"] >= cutoff]
    if not fresh:
        print(f"最近 {args.days} 天无新入库 items，不生成 digest")
        return 0

    lines: dict[str, list[dict]] = {}
    for d in fresh:
        for line in d.get("research_lines") or ["_unlabeled"]:
            lines.setdefault(line, []).append(d)
    rel_rank = {"high": 0, "medium": 1, "low": 2}
    for v in lines.values():
        v.sort(key=lambda d: (rel_rank.get(d["assessment"]["relevance"], 3),
                              d["time"]["published"]), reverse=True)

    # 队列概况
    q_stats = {"pending": 0, "reviewed": 0, "skipped": 0, "skipped_by_llm": 0}
    for p in QUEUE.glob("*.yaml"):
        st = load(p).get("status", "pending")
        q_stats[st if st in q_stats else "pending"] += 1

    today = date.today().isoformat()
    md = [f"# 音视频编码领域 digest（{cutoff} ~ {today}）", ""]
    md.append(f"新入库 **{len(fresh)}** 篇｜基底累计 {len(items)} 篇｜"
              f"队列待审 {q_stats['pending']}、规则跳过 {q_stats['skipped']}、LLM 跳过 {q_stats['skipped_by_llm']}")
    md.append("")

    def line_of(d: dict) -> str:
        ls = [LINE_NAMES.get(l, l) for l in d.get("research_lines", [])]
        return " / ".join(ls) if ls else "未分类"

    for line in [l for l in LINE_ORDER if l in lines] + ["_unlabeled"]:
        if line not in lines:
            continue
        md.append(f"## {LINE_NAMES.get(line, '未分类')}")
        md.append("")
        for d in lines[line]:
            a, s = d["assessment"], d["summaries"]
            n_claims = len(d.get("claims", []))
            deep = f" ｜[深读笔记]({s['deep_dive']})" if s.get("deep_dive") else ""
            md.append(f"- **[{a['relevance']}/{a['decision']}]** "
                      f"[{d.get('title_zh') or d['title']}]({d['source']['url']})"
                      f"{deep}")
            md.append(f"  {s['one_liner_zh']}（{n_claims} 论断）")
        md.append("")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"digest-{today}.md"
    out.write_text("\n".join(md), encoding="utf-8")
    print(f"→ {out}（{len(fresh)} 篇，{sum(len(v) for v in lines.values())} 条目）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
