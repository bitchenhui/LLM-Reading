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
import math
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
复合/范围/定性值一律跳过。只输出 JSON 数组，无有效条目输出 []。原文明确给出时分别填写 setup（锚点版本、配置及固定约束）、basis（质量度量或比较基准）和 statistic（均值、峰值、切片等统计方式）；信息不足的字段留空，禁止推测。"""


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
                    '"metric":"BD-Rate 或指标名","value":数值,"unit":"% 或空","setup":"","basis":"","statistic":""}'
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
            if isinstance(r, dict) and r.get("item") in batch_ids:
                try:
                    r["value"] = float(r["value"])
                    if math.isfinite(r["value"]):
                        cache[r["item"]].append({k: r[k] for k in (*CONDITION_FIELDS, "value") if r.get(k) is not None})
                except (KeyError, TypeError, ValueError):
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
        ("UVG-4K", r"^UVG[ -]?4K$"), ("UVG", r"^UVG(?: 视频基准)?$"),
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


# Broad groups are for browsing. Ranking uses the original, uncollapsed protocol.
CONDITION_FIELDS = ("dataset", "anchor", "metric", "unit", "setup", "basis", "statistic")
DIRECTIONS = {"BD-Rate": "min", "平均码率误差": "min", "码率节省": "max",
              "PSNR": "max", "MS-SSIM": "max", "VMAF": "max"}


def rank_best(entries: list[dict], metric: str) -> float | None:
    if len(entries) < 2 or metric not in DIRECTIONS:
        return None
    first = entries[0]["conditions"]
    if any(not first.get(field) for field in CONDITION_FIELDS):
        return None
    if any(e["conditions"] != first for e in entries[1:]):
        return None
    values = [e["value"] for e in entries]
    return min(values) if DIRECTIONS[metric] == "min" else max(values)


def source_fields(item: dict, row: dict) -> dict:
    """Link only a unique metric with the same name, numeric value and unit."""
    unit = str(row.get("unit") or "").strip()
    matches = []
    for claim in item["claims"]:
        for metric in claim.get("metrics", []):
            name = metric.get("name") or metric.get("ref", "").removeprefix("metric:")
            if name.casefold() != str(row.get("metric") or "").casefold():
                continue
            value = str(metric["value"]).strip()
            declared_unit = str(metric.get("unit") or "").strip()
            if declared_unit and declared_unit != unit:
                continue
            unit_matches = declared_unit == unit or (unit and value.endswith(unit))
            try:
                same_value = float(value.removesuffix(unit).strip()) == row["value"]
            except ValueError:
                continue
            if same_value:
                matches.append((claim, metric.get("scope") or "", unit_matches))
    scopes = {scope for _, scope, _ in matches if scope}
    fields = {"scope": scopes.pop() if len(scopes) == 1 else ""}
    if len(matches) == 1:
        claim, _, unit_matches = matches[0]
        if unit_matches and claim.get("id") and claim.get("evidence_url"):
            fields["claim_id"] = claim["id"]
    return fields


def aggregate(cache: dict, items: dict) -> list:
    groups: dict[tuple, list] = defaultdict(list)
    for iid, rows in cache.items():
        if iid not in items:
            continue
        item = items[iid]
        for r in rows:
            ds, an = norm_dataset(r.get("dataset", "")), norm_anchor(r.get("anchor", ""))
            met = str(r.get("metric", "BD-Rate")).strip().upper().replace(" ", "")
            if met.replace("-", "") == "BDRATE":
                met = "BD-Rate"
            if ds == "—" or an == "—":
                continue
            conditions = {k: str(r.get(k) or "").strip()
                          for k in CONDITION_FIELDS if r.get(k)}
            groups[(ds, an, met)].append({
                "date": item["time"]["published"], "method": item.get("title_zh") or item["title"],
                "value": r["value"], "item": iid, **source_fields(item, r), "conditions": conditions,
            })

    out_groups = []
    for (ds, an, met), entries in sorted(groups.items()):
        if len(entries) < 3:
            continue
        entries.sort(key=lambda e: e["date"])
        out_groups.append({"dataset": ds, "anchor": an, "metric": met, "n": len(entries),
                           "best": rank_best(entries, met), "entries": entries})
    out_groups.sort(key=lambda g: -g["n"])

    return out_groups


def main() -> int:
    ap = argparse.ArgumentParser()
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--rebuild", action="store_true", help="忽略缓存全量重抽")
    mode.add_argument("--cached-only", action="store_true", help="使用现有抽取结果离线重建成绩表")
    args = ap.parse_args()
    if args.cached_only:
        cache = yaml.safe_load(RAW.read_text(encoding="utf-8")) or {}
    else:
        llm = LLM(yaml.safe_load(CONFIG.read_text(encoding="utf-8")))
        llm.req["review_reasoning"] = "low"
        cache = extract_phase(llm, args.rebuild)

    items = {}
    for p in sorted(KB_ITEMS.glob("*.yaml")):
        item = yaml.safe_load(p.read_text(encoding="utf-8"))
        items[item["id"]] = item
    out_groups = aggregate(cache, items)
    doc = {"generated": date.today().isoformat(),
           "note": "仅对原始数据集、锚点、单位、配置、质量基准与统计方式一致且方向明确的组标注最优",
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
