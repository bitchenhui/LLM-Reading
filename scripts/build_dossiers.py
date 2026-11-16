#!/usr/bin/env python3
"""实体档案层（v3 核心）：为关键实体生成滚动档案——"关于 X 我们都知道什么"。

档案 = 注册表静态信息 + 该实体挂接的全部条目（论断/版本/精读摘录）经 glm-5.3 综合：
  ## 档案概览（是什么、谁做的、与谁什么关系）
  ## 关键事实与演进（按时间：版本里程碑 + 技术事实，带口径与引用）
  ## 当前状态与关注点（活跃度、开放问题、生态位）
  ## 近期变化（增量模式：自上版档案以来的新信息）

产出 kb/dossiers/{entity}.md；问答端实体命中时优先引用，前端知识库页展示。
增量逻辑同综述：有旧版且增量 ≤ 上限时走增量修订，零增量保留旧版。

用法：uv run --with pyyaml python scripts/build_dossiers.py [--only impl:VVenC,...] [--full]
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from llm_review import LLM  # noqa: E402

KB_ITEMS = ROOT / "kb" / "items"
KB_ENTITIES = ROOT / "kb" / "entities"
OUT_DIR = ROOT / "kb" / "dossiers"
CONFIG = ROOT / "config" / "llm.local.yaml"
DOS_CONFIG = ROOT / "config" / "dossiers.yaml"

DOSSIER_INSTRUCTIONS = """你是音视频领域知识库的档案管理员，为单个技术实体维护一份滚动档案。
只依据给定资料（注册表信息 + 挂接条目），引用处标 item id，量化结论保留口径，无据推断标「〔档案推断〕」。
结构固定三节：## 档案概览；## 关键事实与演进（按时间线组织，版本里程碑与技术事实交织）；
## 当前状态与关注点（活跃度、开放问题、生态位）。中文，技术密度高，markdown 输出。"""

DOSSIER_INCREMENTAL_INSTRUCTIONS = """你是音视频领域知识库的档案管理员，在增量修订一份实体档案。
你会拿到：上一版档案 + 自那以后新挂接的条目。输出更新后的完整档案（三节结构不变），
主动修订过时表述，并在三节之后追加「## 近期变化」：新信息带来的具体变化清单（引用新 item id），
无实质变化写「无实质变化」。中文，markdown 输出。"""

DELTA_MAX = 80


def load_yaml(p: Path):
    return yaml.safe_load(open(p, encoding="utf-8"))


def safe_name(eid: str) -> str:
    return eid.replace(":", "_")


def pack_items(items: list[dict], with_notes: bool = True, budget: int = 600_000) -> str:
    lines = []
    used = 0
    for d in sorted(items, key=lambda x: x["time"]["published"]):
        if used > budget:
            lines.append(f"…（条目过多，已截断至 {len(lines)} 条，完整清单见 items 层）")
            break
        claims = "".join(
            f"\n    - {c['statement']}" +
            ("".join(f" [{m.get('name') or m.get('ref','').split(':')[-1]}={m.get('value')}"
                     f"{'，'+m['scope'] if m.get('scope') else ''}]" for m in c.get("metrics", [])))
            for c in d.get("claims", [])[:3])
        note = ""
        deep = d["summaries"].get("deep_dive") if with_notes else None
        if deep and (ROOT / deep).exists():
            body = "\n".join((ROOT / deep).read_text(encoding="utf-8").split("\n")[2:])
            note = f"\n  精读摘录: {body[:400]}…"
        kind = "版本" if d["type"] == "repo_release" else ("提案" if d["type"] == "standard_proposal" else "论文")
        line = (f"[{d['time']['published']}|{kind}] {d['id']}｜{d.get('title_zh') or d['title']}"
                f"\n  {d['summaries'].get('one_liner_zh','')}{claims}{note}")
        lines.append(line)
        used += len(line)
    return "\n".join(lines)


def entity_static(e: dict) -> str:
    parts = [f"id: {e['id']}", f"类型: {e['type']}", f"名称: {e['full_name'] if e.get('full_name') else e['name']}"]
    if e.get("aliases"):
        parts.append(f"别名: {', '.join(e['aliases'][:6])}")
    for k in ("status", "first_release", "kind", "notes"):
        if e.get(k):
            parts.append(f"{k}: {e[k]}")
    if e.get("developed_by"):
        parts.append(f"开发方: {', '.join(e['developed_by'])}")
    if e.get("relations"):
        parts.append("静态关系: " + "; ".join(f"{r['type']}→{r['ref']}" for r in e["relations"]))
    if e.get("lower_is_better") is not None:
        parts.append(f"方向: {'越低越好' if e['lower_is_better'] else '越高越好'}")
    return "\n".join(parts)


def prev_cutoff(dom_file: Path) -> str | None:
    if not dom_file.exists():
        return None
    m = re.search(r"数据截止 (\d{4}-\d{2}-\d{2})", dom_file.read_text(encoding="utf-8")[:300])
    return m.group(1) if m else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", type=str, default="", help="只生成指定实体（逗号分隔的 entity id）")
    ap.add_argument("--full", action="store_true", help="强制全量重写")
    ap.add_argument("--low-effort", action="store_true",
                    help="深读用低推理档（大档案防 token 速率墙；汇总类内容够用）")
    args = ap.parse_args()

    cfg = load_yaml(DOS_CONFIG) if DOS_CONFIG.exists() else {}
    min_items = cfg.get("min_items", 5)
    max_entities = cfg.get("max_entities", 30)

    entities: dict[str, dict] = {}
    for p in sorted(KB_ENTITIES.glob("*.yaml")):
        for e in load_yaml(p):
            entities[e["id"]] = e

    linked: dict[str, list[dict]] = defaultdict(list)
    for p in sorted(KB_ITEMS.glob("*/*.yaml")):
        d = load_yaml(p)
        seen_refs = set()
        for link in d.get("entities", []):
            ref = link["ref"]
            if ref in entities and ref not in seen_refs:  # 每条目对每实体只计一次
                linked[ref].append(d)
                seen_refs.add(ref)

    ranked = sorted(linked.items(), key=lambda kv: -len(kv[1]))
    targets = [(eid, its) for eid, its in ranked if len(its) >= min_items][:max_entities]
    if args.only:
        want = {x for x in args.only.split(",") if x}
        targets = [(eid, its) for eid, its in ranked if eid in want]

    print(f"实体档案目标 {len(targets)} 个（阈值 ≥{min_items} 条，上限 {max_entities}）")
    llm = LLM(load_yaml(CONFIG))
    if args.low_effort:
        llm.req["deep_reasoning"] = "low"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()

    for eid, items in targets:
        out_path = OUT_DIR / f"{safe_name(eid)}.md"
        instructions, mode = DOSSIER_INSTRUCTIONS, "全量"
        cutoff = None if args.full else prev_cutoff(out_path)
        delta = [d for d in items if cutoff and d["time"]["collected"] > cutoff] if cutoff else []
        if cutoff and not delta:
            print(f"[{eid}] 自 {cutoff} 无新增，保留旧版")
            continue
        if cutoff and 0 < len(delta) <= DELTA_MAX:
            old = out_path.read_text(encoding="utf-8")
            prompt = (f"实体：{entities[eid]['name']}（{eid}）\n\n上一版档案（数据截止 {cutoff}）：\n{old}\n\n"
                      f"—— 自 {cutoff} 以来新挂接 {len(delta)} 条：\n{pack_items(delta)}\n\n"
                      f"请输出更新后的完整档案（三节 + 近期变化）。")
            instructions, mode = DOSSIER_INCREMENTAL_INSTRUCTIONS, f"增量（+{len(delta)}）"
        else:
            # 大档案（>200 条）自动去掉精读摘录：摘录包过大易触发服务端断流
            use_notes = len(items) <= 200
            prompt = (f"实体：{entities[eid]['name']}（{eid}）\n\n注册表静态信息：\n{entity_static(entities[eid])}\n\n"
                      f"挂接条目 {len(items)} 条：\n{pack_items(items, with_notes=use_notes)}\n\n"
                      f"请生成实体档案（三节结构）。")
        print(f"[{eid}] {len(items)} 条，{mode}，生成中…", flush=True)
        try:
            md = llm.chat(prompt, tier="deep", instructions=instructions, max_tokens=16000)
        except Exception as e:  # noqa: BLE001
            print(f"  ✗ 失败: {e}")
            continue
        md = md.strip().lstrip("```markdown").rstrip("```").strip()
        header = (f"# {entities[eid]['name']} · 实体档案\n\n"
                  f"> {eid} · 数据截止 {today} · 关联 {len(items)} 条 · glm-5.3\n\n")
        out_path.write_text(header + md + "\n", encoding="utf-8")
        print(f"  → {out_path.name}（{len(md)} 字符）", flush=True)

    print(f"\n完成。tokens in={llm.usage['in']} out={llm.usage['out']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
