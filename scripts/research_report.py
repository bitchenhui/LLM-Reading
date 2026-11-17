#!/usr/bin/env python3
"""Deep Research 报告（消费端新形态）：研究主题 → 长篇调研报告（全引用锚定）。

与问答的区别：检索面宽（数十条目+档案+综述）、输出深（六节报告结构、量化对比表）。
流程：
  1. 主题 → 实体命中 + 域识别（复用 ask 的检索机制，扩容打包）
  2. 背景：命中实体的档案 + 对应领域综述
  3. glm-5.3 撰写报告：执行摘要/背景/技术主线与演进/代表工作与量化对比/开放问题/趋势
  4. 落盘 docs/reports/{date}-{slug}.md → 前端「调研报告」区展示

用法：uv run --with pyyaml python scripts/research_report.py "神经视频编码的实用化进程" [--deep-notes]
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from ask import detect_domain, domain_synthesis, entity_dossiers, load_items, rank  # noqa: E402
from fetch_arxiv import entity_patterns, load_entities  # noqa: E402
from llm_review import LLM  # noqa: E402

CONFIG = ROOT / "config" / "llm.local.yaml"
OUT_DIR = ROOT / "docs" / "reports"

REPORT_INSTRUCTIONS = """你是音视频领域的首席研究员，基于知识库资料撰写一篇深度调研报告。
要求：
- 只依据给定资料（实体档案、领域综述、条目及其论断），所有可查证陈述标注来源 item id；
  资料没有的关键判断标「〔报告推断〕」。不编造数字。
- 结构固定六节：# 标题（自拟）；## 执行摘要（≤200字）；## 一、背景与问题定义；
  ## 二、技术主线与演进（按阶段/流派组织）；## 三、代表工作与量化对比（必须含 markdown
  对比表：方法 × 基准 × 结果，保留口径）；## 四、开放问题；## 五、趋势与展望。
- 中文，技术密度高，篇幅 4000-8000 字。markdown 输出。"""


def pack_wide(items: list[dict], with_notes: bool) -> str:
    lines = []
    for d in items:
        claims = "".join(
            f"\n    - {c['statement']}" +
            ("".join(f" [{m.get('name') or m.get('ref','').split(':')[-1]}={m.get('value')}"
                     f"{'，'+m['scope'] if m.get('scope') else ''}]" for m in c.get("metrics", [])))
            for c in d.get("claims", [])[:5])
        note = ""
        deep = d["summaries"].get("deep_dive") if with_notes else None
        if deep and (ROOT / deep).exists():
            body = "\n".join((ROOT / deep).read_text(encoding="utf-8").split("\n")[2:])
            note = f"\n  精读摘录: {body[:600]}…"
        lines.append(f"[{d['time']['published']}] {d['id']}｜{d.get('title_zh') or d['title']}"
                     f"\n  {d['summaries'].get('one_liner_zh','')}"
                     f"\n  摘要: {d['summaries'].get('abstract_zh','')}{claims}{note}")
    return "\n".join(lines)


def slugify(topic: str) -> str:
    ascii_words = re.findall(r"[A-Za-z0-9]+", topic)
    h = abs(hash(topic)) % 10000
    dom = detect_domain(topic) or "report"
    return (dom + "-" + "-".join(ascii_words[:2]) if ascii_words else dom) + f"-{h}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("topic")
    ap.add_argument("--deep-notes", action="store_true", help="包含精读摘录（更慢更贵，质量更高）")
    args = ap.parse_args()

    entities = load_entities()
    pats = entity_patterns(entities)
    items = load_items()
    picked, q_ents = rank(args.topic, items, entities, pats)

    # 扩容检索：排序结果取前 40，再补齐主题域的高相关条目
    picked = picked[:40]
    dom = detect_domain(args.topic)
    if dom:
        have = {d["id"] for d in picked}
        extra = [d for d in items if d.get("domain") == dom
                 and d["assessment"]["relevance"] == "high"
                 and d["id"] not in have][:20]
        picked = picked + extra

    dossiers = entity_dossiers(set(q_ents), limit=2)
    synthesis = domain_synthesis(args.topic, set(q_ents))
    print(f"命中实体 {sorted(q_ents)}｜域 {dom}｜条目 {len(picked)}｜"
          f"档案 {'✓' if dossiers else '—'}｜综述 {'✓' if synthesis else '—'}")

    prompt = (f"研究主题：{args.topic}\n\n"
              + (dossiers + "\n" if dossiers else "")
              + (synthesis + "\n" if synthesis else "")
              + f"【条目资料（{len(picked)} 条）】\n{pack_wide(picked, args.deep_notes)}\n\n"
              f"请撰写深度调研报告。")
    llm = LLM(yaml.safe_load(open(CONFIG, encoding="utf-8")))
    md = llm.chat(prompt, tier="deep", instructions=REPORT_INSTRUCTIONS, max_tokens=30000)
    md = md.strip().lstrip("```markdown").rstrip("```").strip()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    out = OUT_DIR / f"{today}-{slugify(args.topic)}.md"
    header = (f"> 引擎调研报告 · {today} · 基于 {len(picked)} 条条目"
              f"{' + 精读摘录' if args.deep_notes else ''} · glm-5.3\n\n")
    out.write_text(header + md + "\n", encoding="utf-8")
    print(f"→ {out}（{len(md)} 字符，tokens in={llm.usage['in']} out={llm.usage['out']}）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
