#!/usr/bin/env python3
"""时间线事实层（v4）：从基底抽取实体锚定的事实时间线 kb/timeline.yaml。

确定性脚本（无 LLM、可随时重跑、daily 自动刷新）：
  每条 item → 一条事实 {date, entity, kind, fact, evidence, url}
    kind: release（版本）/ research（论文，仅 high 或有精读）/ standard（提案，仅 high）
  entity 取 subject；无 subject 时取首个强类型实体。

消费端：前端「技术时间线」（按月分组、实体过滤）、后续技术雷达。

用法：uv run --with pyyaml python scripts/build_timeline.py
"""
from __future__ import annotations

import sys
from collections import Counter
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
KB_ITEMS = ROOT / "kb" / "items"
OUT = ROOT / "kb" / "timeline.yaml"

STRONG = {"codec_standard", "implementation", "org"}


def subject_of(d: dict, entities: dict | None = None) -> str | None:
    ents = d.get("entities", [])
    for e in ents:
        if e.get("role") == "subject":
            return e["ref"]
    for e in ents:  # 回退：首个强类型实体
        ref = e["ref"]
        t = ref.split(":")[0]
        if t in ("codec", "impl", "org"):
            return ref
    return None


def main() -> int:
    facts = []
    for p in sorted(KB_ITEMS.glob("*/*.yaml")):
        d = yaml.safe_load(open(p, encoding="utf-8"))
        kind = {"repo_release": "release", "standard_proposal": "standard"}.get(d["type"], "research")
        if kind == "research" and not (d["assessment"]["relevance"] == "high"
                                       or d["summaries"].get("deep_dive")):
            continue
        if kind == "standard" and d["assessment"]["relevance"] != "high":
            continue
        ent = subject_of(d)
        if not ent:
            continue
        facts.append({
            "date": d["time"]["published"],
            "entity": ent,
            "kind": kind,
            "fact": d["summaries"].get("one_liner_zh", "") or (d.get("title_zh") or d["title"]),
            "evidence": d["id"],
            "url": d["source"].get("url", ""),
        })
    facts.sort(key=lambda f: (f["date"], f["entity"]), reverse=True)
    doc = {
        "generated": date.today().isoformat(),
        "count": len(facts),
        "by_kind": dict(Counter(f["kind"] for f in facts)),
        "facts": facts,
    }
    OUT.write_text(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=120),
                   encoding="utf-8")
    print(f"→ kb/timeline.yaml（{len(facts)} 条事实：{doc['by_kind']}）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
