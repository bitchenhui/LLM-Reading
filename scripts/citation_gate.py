#!/usr/bin/env python3
"""引用量筛子：对 queue/papers 的 pending 记录批量查 Semantic Scholar 引用数，
做时间归一化的引用门槛——5 年回补"只看权威/高引"的执行层。

门槛逻辑（config/citation.yaml）：
  - 最近 N 天内发表的论文直接放行（引用有时滞，新论文不该被引用数惩罚）
  - 其余：citations >= min_citations（绝对值）或 citations/年 >= min_per_year（时间归一）
  - 不过线 → status=skipped_low_citation（保留记录与引用数，可追溯）
用法：uv run --with pyyaml python scripts/citation_gate.py [--ids-only]
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.request
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
QUEUE = ROOT / "queue" / "papers"
CONFIG = ROOT / "config" / "citation.yaml"
S2 = "https://api.semanticscholar.org/graph/v1/paper/batch?fields=citationCount,year,title"


def s2_batch(arxiv_ids: list[str]) -> dict[str, dict]:
    body = json.dumps({"ids": [f"ARXIV:{i}" for i in arxiv_ids]}).encode()
    for attempt in range(1, 5):
        try:
            req = urllib.request.Request(S2, data=body, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read())
            return {aid: d for aid, d in zip(arxiv_ids, data) if d}
        except Exception as e:  # noqa: BLE001
            wait = 20 * attempt
            print(f"  [S2 {type(e).__name__}] 退避 {wait}s", flush=True)
            time.sleep(wait)
    raise RuntimeError("Semantic Scholar 重试耗尽")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", type=int, default=200)
    args = ap.parse_args()
    cfg = yaml.safe_load(open(CONFIG, encoding="utf-8"))

    pendings = []
    for p in sorted(QUEUE.glob("*.yaml")):
        d = yaml.safe_load(open(p, encoding="utf-8"))
        if d.get("status") == "pending" and not d.get("citation_count"):
            pendings.append((p, d))
    if not pendings:
        print("无待查引用的 pending")
        return 0
    print(f"待查 {len(pendings)} 篇（每批 {args.batch}）")

    today = date.today()
    today_ordinal = today.toordinal()
    n_keep = n_cut = 0
    for i in range(0, len(pendings), args.batch):
        chunk = pendings[i:i + args.batch]
        cites = s2_batch([d["id"].split(":")[-1] for _, d in chunk])
        for p, d in chunk:
            aid = d["id"].split(":")[-1]
            info = cites.get(aid)
            if not info:
                d["citation_count"] = -1   # 查无记录：保守放行（让 LLM 判断）
                keep = True
                note = "S2 无记录"
            else:
                c = info.get("citationCount") or 0
                pub = d["meta"]["published"]
                age_days = max(1, today_ordinal - date.fromisoformat(pub).toordinal())
                d["citation_count"] = c
                d["citation_year"] = info.get("year")
                if age_days <= cfg["recent_days"]:
                    keep = True
                    note = f"新论文放行（{age_days}天，{c} 引）"
                else:
                    per_year = c / (age_days / 365.25)
                    keep = c >= cfg["min_citations"] or per_year >= cfg["min_per_year"]
                    note = f"{c} 引 / {per_year:.1f} 每年"
            if keep:
                n_keep += 1
            else:
                d["status"] = "skipped_low_citation"
                n_cut += 1
            print(f"  [{'保留' if keep else '低引剔除'}] {aid}  {note}")
            yaml.safe_dump(d, open(p, "w", encoding="utf-8"),
                           allow_unicode=True, sort_keys=False, width=100)
        time.sleep(2)  # S2 限速礼貌间隔
        print(f"— 进度 {min(i + args.batch, len(pendings))}/{len(pendings)}")

    print(f"\n引用门槛：保留 {n_keep}，低引剔除 {n_cut}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
