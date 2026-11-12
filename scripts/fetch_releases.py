#!/usr/bin/env python3
"""开源仓库 release adapter（第二信息源）：codec 仓库版本动态 → 候选队列。

与 fetch_arxiv 同构：拉取 → 去重 → 实体对齐打分 → queue/repos/（pending/skipped）。
产出由 llm_review 的 release 分支消费，生成 type=repo_release 的信息项。

传输：优先 gh CLI（认证、限额高），不可用时退回匿名 urllib（GitHub 60/h）。
用法：uv run --with pyyaml python scripts/fetch_releases.py
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import urllib.request
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from fetch_arxiv import entity_patterns, load_entities, match_entities  # noqa: E402

QUEUE = ROOT / "queue" / "repos"
CONFIG = ROOT / "config" / "repos.yaml"


def gh_api(path: str) -> list:
    """优先 gh CLI 认证调用；失败退回匿名 urllib。"""
    try:
        out = subprocess.run(["gh", "api", path], capture_output=True, text=True, timeout=30)
        if out.returncode == 0:
            return json.loads(out.stdout)
    except FileNotFoundError:
        pass
    with urllib.request.urlopen(f"https://api.github.com/{path}", timeout=30,
                                ) as resp:
        return json.loads(resp.read())


def main() -> int:
    cfg = yaml.safe_load(open(CONFIG, encoding="utf-8"))
    weights = yaml.safe_load(open(ROOT / "config" / "arxiv.yaml", encoding="utf-8"))["weights"]
    entities = load_entities()
    pats = entity_patterns(entities)

    QUEUE.mkdir(parents=True, exist_ok=True)
    seen = {p.stem for p in QUEUE.glob("*.yaml")}
    seen |= {p.stem for p in (ROOT / "kb" / "items" / "releases").glob("*.yaml")}

    today = date.today().isoformat()
    n_new = n_pending = n_skipped = 0
    for rcfg in cfg["repos"]:
        repo, subject = rcfg["repo"], rcfg["subject"]
        try:
            rels = gh_api(f"repos/{repo}/releases?per_page={cfg['page_size']}")
        except Exception as e:  # noqa: BLE001
            print(f"  [error] {repo}: {e}")
            continue
        if not isinstance(rels, list) or not rels:
            print(f"  [无 releases] {repo}")
            continue
        for r in rels:
            if r.get("draft"):
                continue
            tag = (r.get("tag_name") or "").strip()
            if not tag:
                continue
            stem = re.sub(r"[^A-Za-z0-9._-]", "-", f"{repo.split('/')[-1]}-{tag}")
            if stem in seen:
                continue
            seen.add(stem)
            body = re.sub(r"\r", "", r.get("body") or "")
            text = f"{r.get('name', '')}\n{body}"
            score, matched = match_entities(text, pats, entities, weights)
            # 主体恒挂接（仓库是精选的）；notes 里命中的实体作补充
            if subject not in {m["ref"] for m in matched} and subject in entities:
                matched.insert(0, {"ref": subject, "count": 1,
                                   "weight": cfg["thresholds"]["pending"]})
                score += cfg["thresholds"]["pending"]
            status = "pending" if score >= cfg["thresholds"]["pending"] else "skipped"
            rec = {
                "id": f"repo_release:github:{stem}",
                "kind": "release",
                "status": status,
                "score": score,
                "matched": matched,
                "meta": {
                    "repo": repo,
                    "tag": tag,
                    "name": r.get("name") or tag,
                    "prerelease": bool(r.get("prerelease")),
                    "published": (r.get("published_at") or "")[:10],
                    "url": r.get("html_url") or f"https://github.com/{repo}/releases/tag/{tag}",
                    "notes": body[:6000],
                },
                "fetched": today,
            }
            yaml.safe_dump(rec, open(QUEUE / f"{stem}.yaml", "w", encoding="utf-8"),
                           allow_unicode=True, sort_keys=False, width=100)
            n_new += 1
            n_pending += status == "pending"
            n_skipped += status == "skipped"
            print(f"  [{status}] {stem}  score={score}")

    print(f"\n新增 release 记录 {n_new}（pending {n_pending} / skipped {n_skipped}），"
          f"队列共 {len(list(QUEUE.glob('*.yaml')))} 条")
    return 0


if __name__ == "__main__":
    sys.exit(main())
