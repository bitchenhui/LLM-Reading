#!/usr/bin/env python3
"""SOTA 追踪表（消费端新形态）：LLM 抽取 + 确定性聚合，产出「基准×锚点」成绩时间序列。

两阶段：
  1. 抽取（glm-flash，带缓存 kb/sota_raw.yaml，按 item 增量）：
     核心域条目 claims 中带数字的指标 → 结构化行 {item, dataset, anchor, metric, value}
  2. 聚合（确定性）：按 (dataset, anchor, metric) 分组，日期排序，标注最优
输出 kb/sota.yaml → 前端 SOTA 追踪表。

用法：uv run --with pyyaml python scripts/build_sota.py [--rebuild]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from collections import defaultdict
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from llm_review import LLM, parse_llm_json  # noqa: E402

KB_ITEMS = ROOT / "kb" / "items" / "papers"
RAW = ROOT / "kb" / "sota_raw.yaml"
OUT = ROOT / "kb" / "sota.yaml"
CONFIG = ROOT / "config" / "llm.local.yaml"

EXTRACT_INSTRUCTIONS = """你是编解码论文实验数据的结构化助手。从给定论断中抽取「可追踪的基准成绩」：
只抽有明确 锚点(对比基线) 与 测试条件(数据集/序列集) 与 单一数值 的条目；
复合/范围/定性值一律跳过。只输出 JSON 数组，无有效条目输出 []。"""


def extract_phase(llm: LLM, rebuild: bool) -> dict:
    cache: dict[str, list] = {}
    if RAW.exists() and not rebuild:
        cache = yaml.safe_load(open(RAW, encoding="utf-8")) or {}

    batch, batch_ids = [], []
    n_new = 0

    def flush():
        nonlocal n_new
        if not batch:
            return
        prompt = ("论断列表（格式：item id | 论断 | 指标标注）：\n"
                  + "\n".join(batch)
                  + '\n\n输出 JSON 数组，每元素 {"item":"...","dataset":"...","anchor":"...",'
                    '"metric":"BD-Rate 或指标名","value":数值,"unit":"% 或空"}'
                    "（value 必须是单个数字；BD-Rate 负值=省码率）")
        try:
            out = llm.chat(prompt, instructions=EXTRACT_INSTRUCTIONS)
            rows = parse_llm_json(out)
            if not isinstance(rows, list):
                rows = []
        except Exception as e:  # noqa: BLE001  该批失败：不写缓存，下次重试
            print(f"  [批次失败，跳过 {len(set(batch_ids))} 篇待重试] {e}")
            return
        for iid in set(batch_ids):
            cache[iid] = []  # 默认空；下面按 item 归位
        for r in rows:
            if isinstance(r, dict) and r.get("item") in cache:
                try:
                    r["value"] = float(r["value"])
                    cache[r["item"]].append({k: r.get(k) for k in
                                             ("dataset", "anchor", "metric", "value", "unit")})
                except (TypeError, ValueError):
                    pass
        n_new += len(set(batch_ids))
        RAW.write_text(yaml.safe_dump(cache, allow_unicode=True, sort_keys=False, width=120),
                       encoding="utf-8")  # 逐批落盘，崩溃可续

    for p in sorted(KB_ITEMS.glob("*.yaml")):
        d = yaml.safe_load(open(p, encoding="utf-8"))
        if d.get("domain", "video_image_coding") != "video_image_coding":
            continue
        if d["id"] in cache:
            continue
        has_metric = any(c.get("metrics") for c in d.get("claims", []))
        if not has_metric:
            cache[d["id"]] = []
            continue
        for c in d.get("claims", []):
            if not c.get("metrics"):
                continue
            ms = "; ".join(f"{m.get('name') or m.get('ref','')}={m.get('value')}"
                           + (f"({m.get('scope')})" if m.get("scope") else "")
                           for m in c["metrics"])
            batch.append(f"{d['id']} | {c['statement']} | {ms}")
            batch_ids.append(d["id"])
        if len(batch) >= 12:
            flush(); batch, batch_ids = [], []
            time.sleep(12)  # 节流：压低 token/分钟，防服务端掐流
    flush()

    RAW.write_text(yaml.safe_dump(cache, allow_unicode=True, sort_keys=False, width=120),
                   encoding="utf-8")
    print(f"抽取完成：{n_new} 篇新处理，缓存覆盖 {len(cache)} 篇")
    return cache


def norm_anchor(a: str) -> str:
    """锚点归一：去版本号/口径后缀，统一到标准名。"""
    a = str(a).strip()
    rules = [
        ("VTM", r"VTM[ -]?\d*"), ("VVenC", r"VVenC[ -]?\d*"), ("VVdec", r"VVde?[Cc]\d*"),
        ("HEVC", r"HEVC(?!-)"), ("VVC", r"VVC(?!-)"), ("AV1", r"\bAV1\b"),
        ("x265", r"x265.*"), ("x264", r"x264.*"), ("HM", r"\bHM\b[ -]?\d*"),
        ("ECM", r"\bECM\b[ -]?\d*"), ("JPEG AI", r"JPEG[ -]?AI"), ("VTM", r"参考模型.*"),
    ]
    for name, pat in rules:
        if re.match(pat, a, re.I):
            return name
    return a.split(",")[0].split("(")[0].strip()[:20] or "—"


def norm_dataset(ds: str) -> str:
    """数据集归一：合并同义写法。"""
    d = str(ds).strip()
    rules = [
        ("Kodak", r"Kodak"), ("CLIC", r"CLIC"), ("Tecnick", r"Tecnick"),
        ("UVG", r"UVG.*(?!4K)"), ("UVG-4K", r"UVG[ -]?4K"),
        ("MCL-JCV", r"MCL[ -]?JCV"), ("VCD", r"VCD"),
        ("JVET CTC", r"(JVET )?(CTC|通用测试序列|标准测试序列|CTC 全类|全类)"),
        ("JVET CTC A", r"CTC.{0,3}A[12]|Class A"),
        ("JVET CTC B", r"CTC.{0,3}B|Class B|HEVC ?B"), ("JVET CTC D", r"CTC.{0,3}D|Class D|HEVC ?D"),
        ("HEVC 测试集", r"HEVC (测试|B~D)"),
    ]
    for name, pat in rules:
        if re.search(pat, d, re.I):
            return name
    return d[:24] or "—"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rebuild", action="store_true", help="忽略缓存全量重抽")
    args = ap.parse_args()

    llm = LLM(yaml.safe_load(open(CONFIG, encoding="utf-8")))
    llm.req["review_reasoning"] = "low"  # 结构化抽取不需要高推理；同时降低 token 吞吐防 TPM 掐流
    cache = extract_phase(llm, args.rebuild)

    titles = {}
    dates = {}
    for p in sorted(KB_ITEMS.glob("*.yaml")):
        d = yaml.safe_load(open(p, encoding="utf-8"))
        titles[d["id"]] = (d.get("title_zh") or d["title"])[:70]
        dates[d["id"]] = d["time"]["published"]

    groups: dict[tuple, list] = defaultdict(list)
    for iid, rows in cache.items():
        for r in rows:
            ds, an = norm_dataset(r.get("dataset", "")), norm_anchor(r.get("anchor", ""))
            met = str(r.get("metric", "BD-Rate")).strip().upper().replace(" ", "")
            if "BDRATE" in met or "BD-RATE" in met.replace("-", ""):
                met = "BD-Rate"
            if ds == "—" or an == "—":
                continue
            groups[(ds, an, met)].append({"date": dates.get(iid, ""), "method": titles.get(iid, iid)[:70],
                                          "value": r["value"], "item": iid})

    out_groups = []
    for (ds, an, met), entries in sorted(groups.items()):
        if len(entries) < 3:
            continue
        entries.sort(key=lambda e: e["date"])
        out_groups.append({"dataset": ds, "anchor": an, "metric": met, "n": len(entries),
                           "best": min(e["value"] for e in entries), "entries": entries})
    out_groups.sort(key=lambda g: -g["n"])

    doc = {"generated": date.today().isoformat(),
           "note": "value 数值口径见原条目；BD-Rate 负值=省码率；best 为组内数值最优，跨组不可比",
           "groups": out_groups,
           "stats": {"items_covered": len(cache), "groups": len(out_groups)}}
    OUT.write_text(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=120),
                   encoding="utf-8")
    print(f"→ kb/sota.yaml（{len(out_groups)} 组）")
    for g in out_groups[:10]:
        print(f"  {g['dataset']} × {g['anchor']} [{g['metric']}]: {g['n']} 条, best {g['best']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
