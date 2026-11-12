#!/usr/bin/env python3
"""语料导出（消费端）：基底 → 微调/继续预训练语料。

分层导出到 corpus/：
  sft_v1.jsonl   逐条目问答对（论文/版本的「它做了什么+关键论断」→ 中文摘要回答）
  docs_v1.jsonl  长文本（自动深读笔记 + 手工精读笔记，纯自产内容，可任意分发）

许可边界（为什么默认只导 arXiv 渠道）：
  - arXiv preprint 许可允许元数据与摘要级使用；我们的 one_liner/claims 是自产改写
  - GitHub release notes 的仓库许可各异（GPL/MIT/自定义），默认排除，--all-channels 打开
用法：uv run --with pyyaml python scripts/export_corpus.py [--all-channels]
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
KB_ITEMS = ROOT / "kb" / "items"
OUT = ROOT / "corpus"


def load(p: Path):
    return yaml.safe_load(open(p, encoding="utf-8"))


def item_qa(d: dict) -> dict:
    """一条 item → 一条 SFT 问答对。"""
    kind = "论文" if d["type"] == "paper" else "版本发布"
    claims = [c["statement"] for c in d.get("claims", [])]
    q = f"{kind}《{d.get('title_zh') or d['title']}》做了什么？关键结果是什么？"
    a = (f"{d['summaries'].get('one_liner_zh', '')}\n\n"
         f"{d['summaries'].get('abstract_zh', '')}\n\n关键论断：\n"
         + "\n".join(f"- {c}" for c in claims)
         + f"\n\n来源: {d['source']['url']}")
    return {"id": d["id"], "type": d["type"], "messages": [
        {"role": "user", "content": q}, {"role": "assistant", "content": a}]}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--all-channels", action="store_true",
                    help="包含 github 等非 arXiv 渠道（注意各仓库 release notes 许可）")
    args = ap.parse_args()

    OUT.mkdir(exist_ok=True)
    today = date.today().isoformat()
    n_sft = n_doc = 0
    with open(OUT / f"sft_v1_{today}.jsonl", "w", encoding="utf-8") as f_sft, \
         open(OUT / f"docs_v1_{today}.jsonl", "w", encoding="utf-8") as f_doc:
        for p in sorted(KB_ITEMS.glob("*/*.yaml")):
            d = load(p)
            ch = d["source"].get("channel")
            if ch != "arxiv" and not args.all_channels:
                continue
            f_sft.write(json.dumps(item_qa(d), ensure_ascii=False) + "\n")
            n_sft += 1
            # 长文本层：深读笔记（自产内容）
            deep = d["summaries"].get("deep_dive")
            if deep and (ROOT / deep).exists():
                text = (ROOT / deep).read_text(encoding="utf-8")
                f_doc.write(json.dumps({"id": d["id"], "source": deep,
                                        "text": text}, ensure_ascii=False) + "\n")
                n_doc += 1
        # 手工精读笔记（人工自产，同样可分发）
        for p in sorted((ROOT / "docs").glob("0*.md")):
            f_doc.write(json.dumps({"id": f"manual:{p.stem}", "source": str(p),
                                    "text": p.read_text(encoding="utf-8")}, ensure_ascii=False) + "\n")
            n_doc += 1

    print(f"→ corpus/sft_v1_{today}.jsonl（{n_sft} 条问答对）")
    print(f"→ corpus/docs_v1_{today}.jsonl（{n_doc} 篇长文）")
    if not args.all_channels:
        print("（仅 arXiv 渠道；--all-channels 可含 GitHub release notes，注意其仓库许可）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
