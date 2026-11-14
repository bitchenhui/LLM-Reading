#!/usr/bin/env python3
"""Via LA 专利池新闻源（standards_ecosystem 域）：via-la.com/news/。

Via LA = MPEG LA 与 Via Licensing 合并后的专利池运营方（AVC/HEVC/VVC/AV1 池），
其新闻页公开可达，是"标准生态-专利许可"线的增量信号源（页面仅展示近期条目，适合
增量跟踪；5 年历史回溯不可得，不作回补）。

用法：uv run --with pyyaml python scripts/fetch_viala.py
"""
from __future__ import annotations

import re
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from fetch_arxiv import entity_patterns, load_entities, match_entities  # noqa: E402
from llm_review import infer_domain  # noqa: E402

QUEUE = ROOT / "queue" / "viala"
URL = "https://www.via-la.com/news/"


def main() -> int:
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    try:
        import certifi
        import ssl
        ctx = ssl.create_default_context(cafile=certifi.where())
        opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx))
        resp = opener.open(req, timeout=30)
    except ImportError:
        resp = urllib.request.urlopen(req, timeout=30)
    with resp:
        h = resp.read().decode("utf-8", errors="replace")

    items = []
    for block in re.findall(r'<div class="news_slider_item">(.*?)</div>\s*</div>\s*</div>', h, re.S):
        link = re.search(r'class="news_slider_item_link" href="([^"]+)"', block)
        d = re.search(r'news_slider_item_date">([^<]+)<', block)
        t = re.search(r"<h3>(.*?)</h3>", block, re.S)
        if link and d and t:
            try:
                date = datetime.strptime(d.group(1).strip(), "%B %d, %Y").isoformat()
            except ValueError:
                continue
            items.append({"url": link.group(1), "date": date,
                          "title": re.sub(r"<[^>]+>|&#\d+;", " ", t.group(1)).strip()})

    entities = load_entities()
    pats = entity_patterns(entities)
    weights = yaml.safe_load(open(ROOT / "config" / "arxiv.yaml", encoding="utf-8"))["weights"]

    QUEUE.mkdir(parents=True, exist_ok=True)
    seen = {p.stem for p in QUEUE.glob("*.yaml")}
    n = 0
    from datetime import date as _date
    today = _date.today().isoformat()
    for it in items:
        stem = re.sub(r"[^A-Za-z0-9._-]", "-", it["url"].rstrip("/").split("/")[-1] or it["date"])
        if not stem or stem in seen:
            continue
        score, matched = match_entities(it["title"], pats, entities, weights)
        # 新闻源本身就是标准生态信号：域按实体推断（提及 VVC/AV1 池 → standards；意外命中其他域也允许）
        status = "pending" if score >= 1 else "skipped"
        rec = {
            "id": f"industry_news:viala:{stem[:60]}",
            "kind": "news",
            "status": status,
            "score": score,
            "matched": matched,
            "meta": {
                "title": it["title"],
                "published": it["date"],
                "url": it["url"],
                "outlet": "Via LA News",
            },
            "fetched": today,
        }
        yaml.safe_dump(rec, open(QUEUE / f"{stem[:60]}.yaml", "w", encoding="utf-8"),
                       allow_unicode=True, sort_keys=False, width=100)
        seen.add(stem)
        n += 1
        print(f"  [{status}] {it['date']} {it['title'][:60]}")
    print(f"\nVia LA 新闻：抓到 {len(items)} 条，新增 {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
