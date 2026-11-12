#!/usr/bin/env python3
"""深度精读阶段：glm-5.3 强档消费 deep_read 候选 → 产出 docs/auto/ 长文精读笔记。

流程：
  1. 从 kb/items/papers/ 选 assessment.decision=deep_read 且尚无 deep_dive 的 items
  2. 下载 PDF 到 paper/（幂等，已存在跳过）
  3. pymupdf 抽取全文
  4. 用同主线/共实体的已有 items 作为「与其他论文的联系」素材
  5. 生成与 docs/ 手工精读同构的笔记 → docs/auto/{arxiv_id}.md
  6. 回写 item 的 summaries.deep_dive，跑基底校验

v1 说明：纯文本深读（不提取论文插图）；笔记为自动档，与手工精读分目录存放。

用法：
  uv run --with pyyaml --with pymupdf python scripts/deep_read.py --limit 2
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import time
import urllib.request
from datetime import date
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from llm_review import LLM  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
KB = ROOT / "kb"
ITEMS = KB / "items" / "papers"
DOCS_AUTO = ROOT / "docs" / "auto"
PAPER_DIR = ROOT / "paper"
CONFIG = ROOT / "config" / "llm.local.yaml"

DEEP_INSTRUCTIONS = """你是音视频/图像编码领域的资深研究员，为领域信息整合引擎撰写论文精读笔记。
要求：
- 忠实原文：所有量化结论必须来自论文文本，带口径（锚点/数据集/条件）；不确定的数字不写。
- 中文、技术密度高：面向该领域研究者，直击方法机理与工程含义，不写科普腔。
- 纯文本环境：不要引用/提及论文插图，不要输出图片占位。
- 笔记全文控制在 6000-9000 字：方法机理写透，实验节保留关键行与结论数字，不逐表抄录。
- 输出 markdown，遵循给定结构，七个小节完整写完。"""

NOTE_TEMPLATE = """# {title}

> {authors}. *arXiv:{external_id} ({pub})*
> 本笔记由引擎自动深读生成（glm-5.3, pipeline deep_read v1），底稿：全文文本

## 1. 背景与动机

## 2. 方法总览

## 3. 关键设计

## 4. 实验结果
（有表格数据时用 markdown 表格呈现关键行）

## 5. 消融要点

## 6. 贡献与启示

## 7. 与其他论文的联系
（仅基于下方「相关论文清单」中有真实关联的条目；没有就不写这一节）
"""


def load_yaml(p: Path):
    return yaml.safe_load(open(p, encoding="utf-8"))


def download_pdf(url: str, dest: Path) -> bool:
    if dest.exists() and dest.stat().st_size > 10240:
        return True
    for attempt in range(1, 4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "LLM-Reading-fetcher/0.1"})
            with urllib.request.urlopen(req, timeout=120) as resp:
                dest.write_bytes(resp.read())
            return dest.stat().st_size > 10240
        except Exception as e:  # noqa: BLE001
            print(f"    [下载失败 {type(e).__name__}] 第 {attempt} 次，60s 后重试", flush=True)
            time.sleep(60)
    return False


def extract_text(pdf: Path) -> str:
    import fitz  # pymupdf

    doc = fitz.open(pdf)
    parts = []
    for i, page in enumerate(doc):
        parts.append(f"===== 第 {i + 1}/{len(doc)} 页 =====\n{page.get_text()}")
    text = "\n".join(parts)
    return text[:400_000]  # 安全上限（glm-5.3 上下文 1M，远够）


def related_items(item: dict, all_items: list[dict], top: int = 8) -> list[dict]:
    mine_ents = {e["ref"] for e in item["entities"]}
    mine_lines = set(item.get("research_lines", []))

    def affinity(o: dict) -> tuple[int, str]:
        if o["id"] == item["id"]:
            return (-1, "")
        shared = mine_ents & {e["ref"] for e in o["entities"]}
        lines = len(mine_lines & set(o.get("research_lines", [])))
        rel = {"high": 3, "medium": 2, "low": 1}.get(o["assessment"]["relevance"], 0)
        return (len(shared) * 2 + lines + rel, o["id"])

    cands = sorted(all_items, key=affinity, reverse=True)[:top]
    return [c for c in cands if affinity(c)[0] > 0]


def build_prompt(item: dict, fulltext: str, related: list[dict]) -> str:
    src, meta = item["source"], item["time"]
    rel_list = "\n".join(
        f"- {r['id']}｜{r['title']}｜{r['summaries'].get('one_liner_zh', '')}"
        for r in related) or "（无）"
    header = NOTE_TEMPLATE.format(
        title=item["title"],
        authors=", ".join(item.get("_authors", ["（见原文）"])),
        external_id=src["external_id"],
        pub=meta["published"],
    )
    return f"""请为以下论文撰写精读笔记，直接输出 markdown 笔记本体（从一级标题开始），结构与示例如下：

{header}

相关论文清单（第 7 节只能从中选确有真实关联的，写清关联依据）：
{rel_list}

论文全文：
{fulltext}"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=2)
    args = ap.parse_args()

    cfg = load_yaml(CONFIG)
    llm = LLM(cfg)
    all_items = [load_yaml(p) | {"_path": p} for p in sorted(ITEMS.glob("*.yaml"))]

    cands = [d for d in all_items
             if d["assessment"]["decision"] == "deep_read" and not d["summaries"].get("deep_dive")]
    cands.sort(key=lambda d: ({"high": 0, "medium": 1, "low": 2}[d["assessment"]["relevance"]],
                              d["time"]["published"]), reverse=True)
    cands = cands[: args.limit]
    print(f"deep_read 候选 {len(cands)} 篇（本次处理）\n")
    if not cands:
        print("无候选（全部已深读或无 deep_read 判定）——正常退出")
        return 0

    today = date.today().isoformat()
    n_ok = 0
    for item in cands:
        arxiv_id = item["id"].split(":")[-1]
        print(f"[{arxiv_id}] {item['title'][:60]}")
        ext = item["source"]["external_id"]  # 2609.01535v2
        pdf = PAPER_DIR / f"{ext}.pdf"
        if not download_pdf(item["source"].get("pdf_url") or f"https://arxiv.org/pdf/{ext}", pdf):
            print("    ✗ PDF 下载失败，跳过")
            continue
        text = extract_text(pdf)
        print(f"    PDF {pdf.name}，全文 {len(text)} 字符")

        # 队列里存过作者信息；item 里没有，从 queue 补
        q = ROOT / "queue" / "papers" / f"{arxiv_id}.yaml"
        if q.exists():
            item["_authors"] = load_yaml(q).get("meta", {}).get("authors", [])
        related = related_items(item, all_items)

        note_path = DOCS_AUTO / f"{arxiv_id}.md"
        try:
            note = llm.chat(build_prompt(item, text, related), tier="deep",
                            instructions=DEEP_INSTRUCTIONS, max_tokens=30000)
        except Exception as e:  # noqa: BLE001
            print(f"    ✗ LLM 失败: {e}")
            continue
        note = re.sub(r"^```(?:markdown)?\s*|\s*```$", "", note.strip())
        DOCS_AUTO.mkdir(exist_ok=True)
        note_path.write_text(note, encoding="utf-8")
        print(f"    → 笔记 {note_path}（{len(note)} 字符）")

        item["summaries"]["deep_dive"] = str(note_path.relative_to(ROOT))
        item["time"]["updated"] = today
        item.pop("_authors", None)
        item.pop("_path", None)
        yaml.safe_dump(item, open(ITEMS / f"{arxiv_id}.yaml", "w", encoding="utf-8"),
                       allow_unicode=True, sort_keys=False, width=100)
        n_ok += 1
        # all_items 里的副本也更新，供后续论文做 related
        for d in all_items:
            if d["id"] == item["id"]:
                d["summaries"]["deep_dive"] = item["summaries"]["deep_dive"]

    print(f"\n完成 {n_ok}/{len(cands)}；tokens in={llm.usage['in']} out={llm.usage['out']}")
    if n_ok:
        print("\n运行基底校验：")
        return subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_kb.py")]).returncode
    return 1


if __name__ == "__main__":
    sys.exit(main())
