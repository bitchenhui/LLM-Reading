#!/usr/bin/env python3
"""JVET 标准提案源（standards_ecosystem 域）：jvet-experts.org DMS 公开区。

发现（2026-11-14 实测）：DMS 的会议文档列表无需登录——
  /doc_end_user/all_meeting.php                    全部会议（id/城市/日期）
  /doc_end_user/current_meeting.php?id_meeting=N   单次会议全部提案（编号/M编号/标题/作者/zip直链）

入库策略（近5年回补 + 增量）分两层，控制量：
  AHG 层：所有 "AHG report"（各专题组进展报告，标准线的权威摘要，每次会议 ~10-15 篇）
  技术层：标题与实体注册表强匹配（score>=3）的具体技术提案，每次会议设上限
产出 queue/jvet/（kind=jvet），由 llm_review 的提案分支审阅。

用法：uv run --with pyyaml python scripts/fetch_jvet.py [--since 2021-10-01] [--meetings 3]
"""
from __future__ import annotations

import argparse
import re
import sys
import time
import urllib.request
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from fetch_arxiv import entity_patterns, load_entities, match_entities  # noqa: E402

BASE = "https://jvet-experts.org/doc_end_user/"
QUEUE = ROOT / "queue" / "jvet"
CONFIG = ROOT / "config" / "jvet.yaml"
UA = {"User-Agent": "Mozilla/5.0 (LLM-Reading standards tracker)"}


def get(url: str) -> str:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def strip_tags(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def fetch_meetings() -> list[dict]:
    """[(id, 城市, 日期)]，按日期倒序。"""
    h = get(BASE + "all_meeting.php")
    rows = re.findall(r'<a href="current_meeting\.php\?id_meeting=(\d+)[^"]*"[^>]*>\s*([^<]+?)\s*</a>(.*?)</tr>', h, re.S)
    out = []
    for mid, city, rest in rows:
        dates = re.findall(r">(\d{4}-\d{2}-\d{2})<", rest)
        if not dates:
            continue
        out.append({"id": int(mid), "city": strip_tags(city), "date": dates[0]})
    out.sort(key=lambda m: m["date"], reverse=True)
    return out


def fetch_meeting_docs(meeting: dict) -> list[dict]:
    h = get(f"{BASE}current_meeting.php?id_meeting={meeting['id']}&search_id_group=1&search_sub_group=1")
    docs = []
    for row in re.findall(r"<tr[^>]*>(.*?)</tr>", h, re.S):
        m = re.search(r'current_document\.php\?id=(\d+)', row)
        if not m:
            continue
        cells = [strip_tags(c) for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row, re.S)]
        cells = [c for c in cells if c]
        if len(cells) < 6 or not cells[0].startswith("JVET-"):
            continue
        docnum = cells[0].replace("\xa0", "").strip()
        title, authors = cells[5], (cells[6] if len(cells) > 6 else "")
        zipm = re.search(r'href="(\.\./doc_end_user/documents/[^"]+\.zip)"', row)
        docs.append({
            "docnum": docnum,
            "mpeg_num": cells[1] if len(cells) > 1 else "",
            "title": title,
            "authors": authors,
            "detail_url": f"{BASE}current_document.php?id={m.group(1)}",
            "zip_url": (BASE + zipm.group(1)[3:]) if zipm else None,
        })
    return docs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", type=str, default="", help="起始日期 YYYY-MM-DD（默认取配置）")
    ap.add_argument("--meetings", type=int, default=0, help="只处理最近 N 次会议（调试用）")
    args = ap.parse_args()

    cfg = yaml.safe_load(open(CONFIG, encoding="utf-8"))
    weights = yaml.safe_load(open(ROOT / "config" / "arxiv.yaml", encoding="utf-8"))["weights"]
    since = args.since or cfg.get("since", "2021-10-01")
    entities = load_entities()
    pats = entity_patterns(entities)

    meetings = fetch_meetings()
    meetings = [m for m in meetings if m["date"] >= since]
    if args.meetings:
        meetings = meetings[: args.meetings]
    print(f"JVET 会议 {len(meetings)} 次（自 {since}），最新: {meetings[0]['city']} {meetings[0]['date']}" if meetings else "无会议")

    QUEUE.mkdir(parents=True, exist_ok=True)
    seen = {p.stem for p in QUEUE.glob("*.yaml")}
    today = date.today().isoformat()
    n_ahg = n_tech = n_skip = 0
    for mt in meetings:
        try:
            docs = fetch_meeting_docs(mt)
        except Exception as e:  # noqa: BLE001
            print(f"  [{mt['city']}] 拉取失败: {e}")
            continue
        meeting_tag = f"{mt['date'][:7]}-{mt['city']}"
        kept_tech = 0
        for d in docs:
            stem = f"m{mt['id']}-{d['docnum'].replace('JVET-', '')}"
            if stem in seen:
                continue
            is_ahg = "AHG report" in d["title"]
            score, matched = match_entities(d["title"], pats, entities, weights)
            status = None
            if is_ahg and score >= 1:
                status = "pending"          # AHG 报告：权威进展摘要
                n_ahg += 1
            elif score >= cfg["thresholds"]["tech_score"] and kept_tech < cfg["thresholds"]["tech_per_meeting"]:
                status = "pending"          # 强匹配技术提案（每次会议限量）
                kept_tech += 1
                n_tech += 1
            else:
                status = "skipped"
                n_skip += 1
            rec = {
                "id": f"standard_proposal:jvet:{stem}",
                "kind": "jvet",
                "status": status,
                "score": score,
                "matched": matched,
                "meta": {
                    "docnum": d["docnum"],
                    "mpeg_num": d["mpeg_num"],
                    "title": d["title"],
                    "authors": d["authors"],
                    "meeting": meeting_tag,
                    "meeting_date": mt["date"],
                    "url": d["detail_url"],
                    "zip_url": d["zip_url"],
                    "is_ahg": is_ahg,
                },
                "fetched": today,
            }
            yaml.safe_dump(rec, open(QUEUE / f"{stem}.yaml", "w", encoding="utf-8"),
                           allow_unicode=True, sort_keys=False, width=100)
            seen.add(stem)
        print(f"  [{meeting_tag}] 文档 {len(docs)}（累计 AHG {n_ahg} / 技术 {n_tech} / 跳过 {n_skip}）")
        time.sleep(3)

    print(f"\n新增 pending：AHG {n_ahg} + 技术 {n_tech}；skipped {n_skip}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
