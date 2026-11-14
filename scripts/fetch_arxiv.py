#!/usr/bin/env python3
"""arXiv 检索 adapter：增量拉取 → 去重 → 实体对齐过滤 → 候选队列。

对应 kb/README.md 入库五步中的 1-3 步（确定性部分）：
  1. 按 config/arxiv.yaml 的 search_query + 时间窗拉取元数据（arXiv Atom API，stdlib 解析）
  2. 去重：arXiv ID 已存在于 kb/items/papers/ 或 queue/papers/ 的跳过
  3. 实体对齐：title+abstract 匹配实体注册表（name/full_name/aliases，词边界），
     按 config 权重打分；达到阈值 → status=pending（待 LLM），否则 status=skipped
产出：queue/papers/{arxiv_id}.yaml（queue 即「已见」记录，天然幂等）
下一步：LLM 阶段消费 pending 记录，产出 kb/items/papers/*.yaml。

用法：
  uv run --with pyyaml python scripts/fetch_arxiv.py                # 默认回看 default_days
  uv run --with pyyaml python scripts/fetch_arxiv.py --days 150     # 补历史
  uv run --with pyyaml python scripts/fetch_arxiv.py --max-results 30
"""
from __future__ import annotations

import argparse
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
KB = ROOT / "kb"
QUEUE = ROOT / "queue" / "papers"
CONFIG = ROOT / "config" / "arxiv.yaml"

ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV_API = "https://export.arxiv.org/api/query"
UA = "LLM-Reading-fetcher/0.1 (mailto:duanchenhui.zoro@jd.com)"  # arXiv 礼貌爬取建议 UA 带联系方式
# 词边界用环视实现，兼容 H.266 / x265 / C3 这类含标点的名字
NAME_RE_CACHE: list[tuple[re.Pattern, str]] | None = None


# ---------- 加载 ----------

def load_yaml(path: Path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_entities() -> dict[str, dict]:
    entities: dict[str, dict] = {}
    for p in sorted((KB / "entities").glob("*.yaml")):
        for e in load_yaml(p):
            entities[e["id"]] = e
    return entities


def seen_ids() -> set[str]:
    """已处理集合 = 已入库 items + 队列记录（含 skipped）。"""
    seen: set[str] = set()
    for d in (KB / "items" / "papers", QUEUE):
        d.mkdir(parents=True, exist_ok=True)
        for p in d.glob("*.yaml"):
            seen.add(p.stem)
    return seen


def entity_patterns(entities: dict[str, dict]) -> list[tuple[re.Pattern, str]]:
    pats = []
    for eid, e in entities.items():
        names = {e["name"], e.get("full_name", ""), *e.get("aliases", [])}
        for n in {n.strip() for n in names if len(n.strip()) >= 2}:
            pats.append((re.compile(rf"(?<![A-Za-z0-9]){re.escape(n)}(?![A-Za-z0-9])",
                                    re.IGNORECASE), eid))
    return pats


# ---------- 匹配与打分 ----------

def match_entities(text: str, pats, entities: dict[str, dict], weights: dict):
    hits: dict[str, int] = {}  # entity_id -> 出现次数
    for pat, eid in pats:
        if pat.search(text):
            hits[eid] = hits.get(eid, 0) + 1
    score = 0
    matched = []
    for eid, count in hits.items():
        w = weights.get(entities[eid]["type"], 0)
        score += w  # 每个实体计一次分，出现次数不叠加（避免高频词灌分）
        matched.append({"ref": eid, "count": count, "weight": w})
    matched.sort(key=lambda m: (-m["weight"], -m["count"], m["ref"]))
    return score, matched


# ---------- arXiv API ----------

def fetch_page(search_query: str, start: int, max_results: int) -> bytes:
    params = {
        "search_query": search_query,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        "start": str(start),
        "max_results": str(max_results),
    }
    url = ARXIV_API + "?" + urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    last_err: Exception | None = None
    for attempt in range(1, 6):  # 429/超时退避：60s 起，最多 5 次
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.read()
        except urllib.error.HTTPError as e:
            last_err = e
            if e.code == 429:
                wait = 60 * attempt
                print(f"  [429 限流] 第 {attempt} 次退避 {wait}s…", flush=True)
                time.sleep(wait)
                continue
            raise RuntimeError(f"arXiv API HTTP {e.code}: {url}") from e
        except Exception as e:  # noqa: BLE001
            last_err = e
            wait = 30 * attempt
            print(f"  [网络异常 {type(e).__name__}] 退避 {wait}s…", flush=True)
            time.sleep(wait)
    raise RuntimeError(f"arXiv API 重试耗尽: {url}\n{last_err}")


def parse_atom(xml: bytes) -> list[dict]:
    root = ET.fromstring(xml)
    out = []
    for entry in root.findall(f"{ATOM}entry"):
        raw_id = entry.findtext(f"{ATOM}id", "")  # http://arxiv.org/abs/2606.12345v2
        m = re.search(r"abs/([0-9.]+)(v\d+)?$", raw_id)
        if not m:
            continue
        links = {l.get("title"): l.get("href") for l in entry.findall(f"{ATOM}link")}
        out.append({
            "arxiv_id": m.group(1),
            "version": m.group(2) or "",
            "title": re.sub(r"\s+", " ", entry.findtext(f"{ATOM}title", "")).strip(),
            "abstract": re.sub(r"\s+", " ", entry.findtext(f"{ATOM}summary", "")).strip(),
            "authors": [a.findtext(f"{ATOM}name", "") for a in entry.findall(f"{ATOM}author")],
            "published": entry.findtext(f"{ATOM}published", "")[:10],
            "updated": entry.findtext(f"{ATOM}updated", "")[:10],
            "categories": [c.get("term", "") for c in entry.findall(f"{ATOM}category")],
            "url": f"https://arxiv.org/abs/{m.group(1)}",
            "pdf_url": links.get("pdf") or f"https://arxiv.org/pdf/{m.group(1)}",
        })
    return out


# ---------- 主流程 ----------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, help="回看天数（覆盖 config 的 default_days）")
    ap.add_argument("--since", type=str, help="起始日 YYYYMMDD（优先于 --days）")
    ap.add_argument("--max-results", type=int, default=200, help="本次最多处理条数")
    ap.add_argument("--per-track", type=int, default=0, help="单 track 上限（0=用配置；5年回补时调大）")
    args = ap.parse_args()

    cfg = load_yaml(CONFIG)
    entities = load_entities()
    pats = entity_patterns(entities)
    seen = seen_ids()

    now = datetime.now()
    if args.since:
        since = args.since
    else:
        days = args.days or cfg["default_days"]
        since = (now - timedelta(days=days)).strftime("%Y%m%d%H%M")
    until = now.strftime("%Y%m%d%H%M")

    # 多 track（领域分类）检索；兼容旧版单 search_query 配置
    tracks = cfg.get("tracks") or [{"name": "video_image_coding", "core": True,
                                    "search_query": cfg["search_query"]}]
    per_track_max = args.per_track or cfg.get("per_track_max", args.max_results)

    print(f"窗口 {since[:8]}..{until[:8]}，已处理 {len(seen)} 篇")
    entries: list[dict] = []
    seen_in_run: set[str] = set()
    for tr in tracks:
        query = f'({tr["search_query"]}) AND submittedDate:[{since} TO {until}]'
        tr_threshold = tr.get("threshold", cfg["thresholds"]["pending"])
        cap = min(per_track_max, args.max_results)
        tr_entries: list[dict] = []
        start = 0
        while start < cap:
            page = parse_atom(fetch_page(query, start, min(cfg["page_size"], cap - start)))
            tr_entries.extend(page)
            if len(page) < min(cfg["page_size"], cap - start):
                break
            start += len(page)
            time.sleep(3)  # arXiv 礼貌间隔
        tr_entries = [e for e in tr_entries if e["arxiv_id"] not in seen_in_run]
        seen_in_run.update(e["arxiv_id"] for e in tr_entries)
        for e in tr_entries:
            e["track"] = tr["name"]
            e["_threshold"] = tr_threshold
        entries.extend(tr_entries)
        print(f"  [{tr['name']}] 命中 {len(tr_entries)}")

    new = [e for e in entries if e["arxiv_id"] not in seen]
    print(f"合计命中 {len(entries)}，去重后新增 {len(new)}")

    n_pending = n_skipped = 0
    for e in new:
        text = e["title"] + "\n" + e["abstract"]
        score, matched = match_entities(text, pats, entities, cfg["weights"])
        status = "pending" if score >= e.get("_threshold", cfg["thresholds"]["pending"]) else "skipped"
        rec = {
            "id": f"paper:arxiv:{e['arxiv_id']}",
            "status": status,          # pending=待 LLM 精读过滤 / skipped=规则拒绝
            "score": score,
            "track": e.get("track", "video_image_coding"),  # 领域分类（检索口径给的初值）
            "matched": matched,
            "meta": {
                "title": e["title"],
                "authors": e["authors"],
                "published": e["published"],
                "updated": e["updated"],
                "categories": e["categories"],
                "abstract": e["abstract"],
                "url": e["url"],
                "pdf_url": e["pdf_url"],
                "version": e["version"],
            },
            "fetched": now.strftime("%Y-%m-%d"),
        }
        with open(QUEUE / f"{e['arxiv_id']}.yaml", "w", encoding="utf-8") as f:
            yaml.safe_dump(rec, f, allow_unicode=True, sort_keys=False, width=100)
        if status == "pending":
            n_pending += 1
        else:
            n_skipped += 1
        top = ", ".join(m["ref"] for m in matched[:4]) or "-"
        print(f"  [{status:<7}] {e['arxiv_id']}  score={score:<2} ({top})  {e['title'][:60]}")

    print(f"\n新增 pending {n_pending} / skipped {n_skipped}，队列共 {len(list(QUEUE.glob('*.yaml')))} 条")
    return 0


if __name__ == "__main__":
    sys.exit(main())
