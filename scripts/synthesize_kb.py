#!/usr/bin/env python3
"""知识库合成器（v2 核心）：对每个领域大类，基于截至当前的全部 items，
用 glm-5.3 提炼「发展历程 / 技术主线与代表工作 / 当前关键问题 / 趋势」，
产出 kb/synthesis/{domain}.md —— 这就是知识库的综述层（问答与前端知识页的骨架）。

诚实性约束：只依据给定条目，引用 item id；无据的推断显式标注为「综述推断」。
重跑（daily 积累后刷新）：uv run --with pyyaml python scripts/synthesize_kb.py [--only video_image_coding]
"""
from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from llm_review import LLM  # noqa: E402

KB_ITEMS = ROOT / "kb" / "items"
OUT_DIR = ROOT / "kb" / "synthesis"
CONFIG = ROOT / "config" / "llm.local.yaml"

DOMAIN_NAMES = {
    "video_image_coding": "视频/图像编码",
    "audio_coding": "音频编码",
    "streaming_delivery": "流媒体传输",
    "quality_assessment": "质量评估",
    "processing_enhancement": "处理增强",
    "immersive_media": "沉浸式与三维",
    "standards_ecosystem": "标准生态",
    "self_improvement": "自我改进 AI（RSI/EoH）",
}
DOMAIN_ORDER = list(DOMAIN_NAMES)

SYNTH_INSTRUCTIONS = """你是音视频技术领域的首席研究员，为一个垂类知识库撰写领域综述。
要求：
- 只依据给定的条目资料（截至给定日期的全部数据），引用处标 item id（如 paper:arxiv:26xx.xxxxx 或 repo_release:github:xxx）。
- 条目没覆盖的判断若确有必要给出，显式标注「〔综述推断〕」。
- 结构固定为四节：## 发展历程（按时间阶段，含版本里程碑）；## 技术主线与代表工作；## 当前关键问题（具体到技术点，这是最重要的部分）；## 趋势与展望。
- 量化结论保留条目里的口径。中文，技术密度高，markdown 输出。"""

INCREMENTAL_INSTRUCTIONS = """你是音视频技术领域的首席研究员，在维护一个垂类知识库的领域综述（增量修订模式）。
你会拿到：上一版综述 + 自那以后新入库的条目。请输出更新后的完整综述：
- 四节结构不变（发展历程/技术主线/关键问题/趋势），融合新信息，主动修订过时表述——
  新证据刷新了旧结论的地方要改写，不要保留已知过时的说法。
- 引用新增条目时标 item id；无据推断标「〔综述推断〕」；量化结论保留口径。
- 四节之后追加一节「## 本周演进」：这次新信息带来的具体认知变化清单——哪些结论被
  强化/修正/新增、出现了什么新问题，逐条引用新 item id。没有实质变化就写「无实质演进」。
- 中文，技术密度高，markdown 输出。"""

DELTA_MAX = 150   # 增量超过此数则回退全量重写（避免巨大的增量包）


def prev_cutoff(dom: str) -> str | None:
    """旧综述头部的数据截止日期；无旧版返回 None。"""
    p = OUT_DIR / f"{dom}.md"
    if not p.exists():
        return None
    import re
    m = re.search(r"数据截止 (\d{4}-\d{2}-\d{2})", p.read_text(encoding="utf-8")[:300])
    return m.group(1) if m else None


def pack_domain(items: list[dict], with_notes: bool = True) -> str:
    lines = []
    for d in sorted(items, key=lambda x: x["time"]["published"]):
        claims = "".join(
            f"\n    - {c['statement']}" +
            ("".join(f" [{m.get('name') or m.get('ref','').split(':')[-1]}={m.get('value')}"
                     f"{'，'+m['scope'] if m.get('scope') else ''}]" for m in c.get("metrics", [])))
            for c in d.get("claims", [])[:4])
        note = ""
        deep = d["summaries"].get("deep_dive") if with_notes else None
        if deep and (ROOT / deep).exists():
            text = (ROOT / deep).read_text(encoding="utf-8")
            # 去掉自动生成头两行，取笔记开头的方法动机部分
            body = "\n".join(text.split("\n")[2:])
            note = f"\n  精读摘录: {body[:500]}…"
        lines.append(f"[{d['time']['published']}] {d['id']}｜{d.get('title_zh') or d['title']}"
                     f"\n  摘要: {d['summaries'].get('one_liner_zh','')}{claims}{note}")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", type=str, default="", help="只合成指定 domain（逗号分隔）")
    ap.add_argument("--no-notes", action="store_true", help="跳过精读摘录（排障用）")
    ap.add_argument("--full", action="store_true", help="强制全量重写（忽略旧版综述）")
    args = ap.parse_args()

    llm = LLM(yaml.safe_load(open(CONFIG, encoding="utf-8")))
    only = {x for x in args.only.split(",") if x}

    by_domain: dict[str, list[dict]] = {}
    for p in sorted(KB_ITEMS.glob("*/*.yaml")):
        d = yaml.safe_load(open(p, encoding="utf-8"))
        by_domain.setdefault(d.get("domain", "video_image_coding"), []).append(d)

    today = date.today().isoformat()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for dom in DOMAIN_ORDER:
        if dom not in by_domain or not by_domain[dom]:
            print(f"[{dom}] 无条目，跳过")
            continue
        if only and dom not in only:
            continue
        items = by_domain[dom]
        instructions, mode = SYNTH_INSTRUCTIONS, "全量"
        cutoff = None if args.full else prev_cutoff(dom)
        delta = [d for d in items
                 if cutoff and d["time"]["collected"] > cutoff] if cutoff else []
        if cutoff and not delta and not args.full:
            print(f"[{dom}] 自 {cutoff} 无新增，保留旧版")
            continue

        if cutoff and 0 < len(delta) <= DELTA_MAX:
            old = (OUT_DIR / f"{dom}.md").read_text(encoding="utf-8")
            prompt = (f"领域：{DOMAIN_NAMES[dom]}（{dom}）\n"
                      f"上一版综述（数据截止 {cutoff}，全库共 {len(items)} 条）：\n\n{old}\n\n"
                      f"—— 自 {cutoff} 以来新入库 {len(delta)} 条：\n\n"
                      f"{pack_domain(delta, with_notes=not args.no_notes)}\n\n"
                      f"请按增量修订模式输出更新后的完整综述（四节 + 本周演进）。")
            instructions, mode = INCREMENTAL_INSTRUCTIONS, f"增量（+{len(delta)} 条）"
        else:
            prompt = (f"领域：{DOMAIN_NAMES[dom]}（{dom}）\n"
                      f"数据截止：{today}，共 {len(items)} 条（论文+版本动态）。\n\n"
                      f"条目资料：\n{pack_domain(items, with_notes=not args.no_notes)}\n\n"
                      f"请撰写该领域综述（四节结构）。")

        print(f"[{dom}] {len(items)} 条，{mode}，合成中…", flush=True)
        try:
            md = llm.chat(prompt, tier="deep", instructions=instructions,
                          max_tokens=24000)
        except Exception as e:  # noqa: BLE001
            print(f"  ✗ 失败: {e}")
            continue
        md = md.strip().lstrip("```markdown").rstrip("```").strip()
        header = (f"# {DOMAIN_NAMES[dom]} · 领域综述\n\n"
                  f"> 引擎合成 · 数据截止 {today} · 基于 {len(items)} 条结构化条目 · glm-5.3\n\n")
        (OUT_DIR / f"{dom}.md").write_text(header + md + "\n", encoding="utf-8")
        print(f"  → kb/synthesis/{dom}.md（{len(md)} 字符，tokens {llm.usage}）", flush=True)

    print(f"\n完成。tokens in={llm.usage['in']} out={llm.usage['out']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
