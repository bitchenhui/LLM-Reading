#!/usr/bin/env python3
"""RAG 问答（消费端）：垂类专家读取端——基底 + 基座模型。

检索策略 v0（实体优先，无向量库——垂类实体闭集让这成为可能）：
  1. 问题与实体注册表 name/aliases 词边界匹配 → 问题实体集
  2. 候选 = 挂接任一问题实体的 items；按 (实体重合加权, 相关性, 时近性, 有无深读) 排序
  3. 问题无实体命中时，按研究主线中文名/关键词回退到近期高相关 items
  4. 打包 top-K：one_liner + 论断（带口径）+ 摘要；带深读笔记的取笔记摘录
  5. glm-5.3 作答：要求引用 item id，明确区分「基底有据」与「一般知识补充」

用法：
  uv run --with pyyaml python scripts/ask.py "近半年 VVenC 有哪些值得关注的优化？"
  uv run --with pyyaml python scripts/ask.py "..." --show-context   # 调试检索命中
"""
from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from fetch_arxiv import entity_patterns, load_entities  # noqa: E402
from llm_review import DOMAIN_MARKERS, LLM  # noqa: E402

SYNTH_DIR = ROOT / "kb" / "synthesis"

KB_ITEMS = ROOT / "kb" / "items"
DOSSIER_DIR = ROOT / "kb" / "dossiers"
CONFIG = ROOT / "config" / "llm.local.yaml"

# 域名/中文关键词 → 领域（问题没命中实体时的域识别）；具体域先于核心域判断
DOMAIN_KEYWORDS = [
    ("streaming_delivery", ["流媒体", "传输", "低延迟", "DASH", "WebRTC", "ABR"]),
    ("audio_coding", ["音频", "语音", "音频编码"]),
    ("quality_assessment", ["质量评估", "VQA", "IQA", "QoE", "画质"]),
    ("processing_enhancement", ["超分", "后滤波", "增强"]),
    ("immersive_media", ["沉浸", "点云", "NeRF", "3DGS", "三维", "光场"]),
    ("standards_ecosystem", ["标准", "专利", "许可", "JVET", "提案"]),
    ("self_improvement", ["自我改进", "自改进", "RSI", "EoH", "self-improvement"]),
    ("video_image_coding", ["编码", "压缩", "codec", "视频", "图像"]),
]


def detect_domain(question: str) -> str | None:
    for dom, kws in DOMAIN_KEYWORDS:
        if any(k in question for k in kws):
            return dom
    return None

ASK_INSTRUCTIONS = """你是音视频/图像编码领域的专家助手，回答基于给定的「基底资料」。
要求：
- 优先用基底资料回答，引用来源时用其 id（如 paper:arxiv:2606.28027、repo_release:github:SVT-AV1-v4.0.0）。
- 量化结论保留口径（锚点/数据集/条件），基底里没有的数字不要编。
- 基底未覆盖的部分可以补充一般知识，但必须显式标注「基底未覆盖，以下为一般知识」。
- 中文回答，条理清晰，不啰嗦。"""

LINE_KEYWORDS = {  # 研究主线中文名 → line id（问题未命中实体时的回退）
    "传统编码器优化": "traditional_codec_opt", "VVenC": "traditional_codec_opt",
    "学习式编码": "learned_codec", "神经编码": "learned_codec",
    "面向机器": "coding_for_machines", "生成式": "generative_compression",
    "扩散": "generative_compression", "INR": "inr_representation", "隐式表示": "inr_representation",
    "部署": "systems_deployment", "NPU": "systems_deployment",
}
STRONG_TYPES = {"codec_standard", "implementation"}


def load_items() -> list[dict]:
    items = []
    for p in sorted(KB_ITEMS.glob("*/*.yaml")):
        d = yaml.safe_load(open(p, encoding="utf-8"))
        d["_ents"] = {e["ref"] for e in d.get("entities", [])}
        items.append(d)
    return items


def rank(question: str, items: list[dict], entities: dict, pats) -> tuple[list[dict], list[str]]:
    q_ents = {eid for pat, eid in pats if pat.search(question)}
    line_hit = next((l for k, l in LINE_KEYWORDS.items() if k in question), None)
    today = date.today()
    # 意图感知：问版本/发布 → release 加权；问论文/方法 → paper 加权；问题点名领域 → 该域加权
    rel_intent = any(k in question for k in ("版本", "发布", "更新", "release", "上线", "changelog"))
    paper_intent = any(k in question for k in ("论文", "原理", "方法", "研究", "提出"))
    dom_hint = detect_domain(question)

    def score(d: dict) -> tuple:
        overlap = d["_ents"] & q_ents
        w = sum(3 if entities.get(e, {}).get("type") in STRONG_TYPES else 1 for e in overlap)
        s = w * 3
        s += {"high": 4, "medium": 2, "low": 0}.get(d["assessment"]["relevance"], 0)
        if dom_hint and d.get("domain") == dom_hint:
            s += 3
        pub = d["time"]["published"]
        if (today.isoformat() > pub) and (int(today.strftime("%Y%m%d")) - int(pub.replace("-", "")) < 270):
            s += 2
        if d["summaries"].get("deep_dive"):
            s += 1
        if line_hit and line_hit in d.get("research_lines", []):
            s += 2
        if rel_intent and d["type"] == "repo_release":
            s += 8
        if paper_intent and d["type"] == "paper":
            s += 3
        return (s, pub)

    def subject(d: dict) -> str:
        for e in d.get("entities", []):
            if e["role"] == "subject":
                return e["ref"]
        return d["id"]

    def diverse(ranked: list[dict], k: int, per_subject: int = 3) -> list[dict]:
        """同一主体最多 per_subject 条，避免某仓库/某模型的版本流霸屏上下文。"""
        picked, quota = [], {}
        for d in ranked:
            s = subject(d)
            if quota.get(s, 0) >= per_subject:
                continue
            quota[s] = quota.get(s, 0) + 1
            picked.append(d)
            if len(picked) >= k:
                break
        return picked or ranked[:k]

    if q_ents or line_hit or dom_hint:
        ranked = sorted(items, key=score, reverse=True)
        picked = diverse([d for d in ranked if score(d)[0] > 2], 8) or diverse(ranked, 5)
    else:  # 无信号：近期高相关兜底
        ranked = sorted(items, key=lambda d: (d["time"]["published"], d["assessment"]["relevance"]),
                        reverse=True)
        picked = diverse(ranked, 5)
    return picked, sorted(q_ents)


def pack_context(picked: list[dict]) -> str:
    blocks = []
    for d in picked:
        claims = []
        for c in d.get("claims", [])[:6]:
            ms = "".join(f" [{m.get('name') or m.get('ref','').split(':')[-1]}={m.get('value')}"
                         f"{m.get('scope','') and '，'+m['scope']}]" for m in c.get("metrics", []))
            claims.append(f"  - {c['statement']}{ms}")
        deep = d["summaries"].get("deep_dive")
        note = ""
        if deep and (ROOT / deep).exists():
            note = "\n  [深读笔记摘录] " + (ROOT / deep).read_text(encoding="utf-8")[:1200]
        blocks.append(
            f"### {d['id']}\n标题: {d.get('title_zh') or d['title']}\n"
            f"日期: {d['time']['published']}｜{d['assessment']['relevance']}/{d['assessment']['decision']}\n"
            f"一句话: {d['summaries'].get('one_liner_zh','')}\n"
            + ("论断:\n" + "\n".join(claims) + "\n" if claims else "")
            + note)
    return "\n\n".join(blocks)


def domain_synthesis(question: str, q_ents: set[str]) -> str | None:
    """问题 → 领域（先按中文关键词，再按命中实体）→ 对应领域的综述背景。"""
    dom = detect_domain(question)
    if dom is None:
        from llm_review import CORE_DOMAIN
        for d, markers in DOMAIN_MARKERS:
            if q_ents & markers:
                dom = d
                break
        if dom is None and q_ents:
            dom = CORE_DOMAIN
    if not dom:
        return None
    p = SYNTH_DIR / f"{dom}.md"
    if p.exists():
        text = p.read_text(encoding="utf-8")
        return f"【领域综述背景（引擎合成，供全局背景，具体论断仍以下面条目为准）】\n{text[:12000]}\n"
    return None


def entity_dossiers(q_ents: set[str], limit: int = 2) -> str:
    """问题命中的实体 → 优先取实体档案（最高浓度的单实体知识）。"""
    parts = []
    for ref in sorted(q_ents, key=lambda r: (0 if r.startswith(("codec:", "impl:")) else 1)):
        p = DOSSIER_DIR / f"{ref.replace(':', '_')}.md"
        if p.exists():
            parts.append(f"【实体档案：{ref}（引擎维护的滚动档案）】\n{p.read_text(encoding='utf-8')[:8000]}\n")
        if len(parts) >= limit:
            break
    return "\n".join(parts)


def answer_question(question: str) -> dict:
    """检索 + 作答。供 CLI 与 serve.py 复用。"""
    entities = load_entities()
    pats = entity_patterns(entities)
    items = load_items()
    picked, q_ents = rank(question, items, entities, pats)
    dossiers = entity_dossiers(set(q_ents))
    background = domain_synthesis(question, set(q_ents))
    context = pack_context(picked)
    llm = LLM(yaml.safe_load(open(CONFIG, encoding="utf-8")))
    prompt = (f"问题：{question}\n\n"
              + (dossiers + "\n" if dossiers else "")
              + (background + "\n" if background else "")
              + f"【条目资料】\n{context}")
    answer = llm.chat(prompt, tier="deep", instructions=ASK_INSTRUCTIONS, max_tokens=8000)
    return {
        "answer": answer,
        "q_ents": q_ents,
        "used": [d["id"] for d in picked],
        "tokens": dict(llm.usage),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("question")
    ap.add_argument("--show-context", action="store_true")
    args = ap.parse_args()

    entities = load_entities()
    pats = entity_patterns(entities)
    items = load_items()
    picked, q_ents = rank(args.question, items, entities, pats)
    print(f"命中实体: {q_ents or '（无，按时间/相关性回退）'}")
    print(f"检索打包 {len(picked)} 条: " + ", ".join(d["id"].split(":")[-1] for d in picked))
    if args.show_context:
        print("\n" + pack_context(picked) + "\n---")
    r = answer_question(args.question)
    print("\n" + r["answer"])
    print(f"\n— tokens in={r['tokens']['in']} out={r['tokens']['out']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
