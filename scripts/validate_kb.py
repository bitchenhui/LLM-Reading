#!/usr/bin/env python3
"""校验 kb/ 基底的一致性。

kb/schema/*.json 是权威契约，本脚本实现与契约等价的检查（不依赖 jsonschema）：
  - 实体：必填字段、id 前缀与 type 一致、id 全局唯一、relations/developed_by 引用可解析
  - 信息项：必填字段、id 的 type/channel 与内容一致、实体/指标/关系引用可解析、
    deep_dive 指向的精读笔记存在、日期格式、词表枚举
用法：python3 scripts/validate_kb.py   （依赖 PyYAML）
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
KB = ROOT / "kb"

ITEM_TYPES = {
    "paper", "standard_proposal", "standard_update", "repo_release", "blog",
    "benchmark_report", "patent", "industry_news", "dataset_release",
}
ENTITY_PREFIX_TYPE = {
    "codec": "codec_standard", "org": "org", "impl": "implementation",
    "dataset": "dataset", "metric": "metric", "concept": "concept",
}
ROLES = {"subject", "uses", "builds_on", "evaluated_on", "measured_by",
         "compared_against", "affiliation", "platform"}
RELATION_TYPES = {"cites", "builds_on", "improves_on", "compares_with",
                  "same_topic", "complements", "contrasts_with"}
CONFIDENCE = {"reported", "verified", "inferred"}
RELEVANCE = {"high", "medium", "low"}
DECISIONS = {"deep_read", "summary_only", "skip"}
RESEARCH_LINES = {"traditional_codec_opt", "learned_codec", "coding_for_machines",
                  "generative_compression", "inr_representation", "systems_deployment"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ITEM_ID_RE = re.compile(r"^[a-z_]+:[a-z0-9_.-]+:[A-Za-z0-9_.+-]+$")

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def load_yaml_files(pattern: str) -> list[tuple[Path, dict]]:
    out = []
    for p in sorted(KB.rglob(pattern)):
        with open(p, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        out.append((p, data))
    return out


def main() -> int:
    # ---------- 实体 ----------
    entity_files = load_yaml_files("entities/*.yaml")
    entities: dict[str, tuple[Path, dict]] = {}
    for path, docs in entity_files:
        if not isinstance(docs, list):
            err(f"{path}: 应为实体列表")
            continue
        for e in docs:
            missing = [k for k in ("id", "type", "name") if k not in e]
            if missing:
                err(f"{path}: 实体缺必填字段 {missing}: {e}")
                continue
            eid = e["id"]
            prefix = eid.split(":", 1)[0]
            if prefix not in ENTITY_PREFIX_TYPE or ENTITY_PREFIX_TYPE[prefix] != e["type"]:
                err(f"{path}: id 前缀与 type 不匹配: {eid} type={e['type']}")
            if eid in entities:
                err(f"实体 id 重复: {eid}（{entities[eid][0]} 与 {path}）")
            entities[eid] = (path, e)

    # 实体间引用
    for eid, (path, e) in entities.items():
        for ref in e.get("developed_by", []):
            if ref not in entities:
                err(f"{path} {eid}: developed_by 引用不存在: {ref}")
        for rel in e.get("relations", []):
            if rel.get("ref") not in entities:
                err(f"{path} {eid}: relations 引用不存在: {rel.get('ref')}")

    # ---------- 信息项 ----------
    item_files = load_yaml_files("items/**/*.yaml")
    items: dict[str, tuple[Path, dict]] = {}
    for path, doc in item_files:
        if not isinstance(doc, dict):
            err(f"{path}: 应为单个信息项映射")
            continue
        missing = [k for k in ("id", "type", "title", "source", "time", "entities",
                               "claims", "summaries", "assessment", "provenance")
                   if k not in doc]
        if missing:
            err(f"{path}: 缺必填字段 {missing}")
            continue
        iid = doc["id"]
        if iid in items:
            err(f"信息项 id 重复: {iid}")
        items[iid] = (path, doc)

    # 信息项内容检查
    n_claims = n_metrics = 0
    for iid, (path, d) in items.items():
        if d["type"] not in ITEM_TYPES:
            err(f"{path}: type 非法: {d['type']}")
        parts = iid.split(":")
        if len(parts) != 3 or parts[0] != d["type"]:
            err(f"{path}: id 的 type 段与 type 字段不一致: {iid}")
        if len(parts) == 3 and parts[1] != d["source"].get("channel"):
            err(f"{path}: id 的 channel 段与 source.channel 不一致: {iid} vs {d['source'].get('channel')}")
        if "url" not in d["source"]:
            err(f"{path}: source 缺 url")

        t = d["time"]
        for k in ("published", "collected"):
            if not DATE_RE.match(str(t.get(k, ""))):
                err(f"{path}: time.{k} 应为 YYYY-MM-DD（YAML 记得加引号）: {t.get(k)!r}")
        if not DATE_RE.match(str(d["provenance"].get("created", ""))):
            err(f"{path}: provenance.created 应为 YYYY-MM-DD: {d['provenance'].get('created')!r}")

        for line in d.get("research_lines", []):
            if line not in RESEARCH_LINES:
                err(f"{path}: research_line 非法: {line}")

        if not d["entities"]:
            err(f"{path}: entities 不能为空")
        for link in d["entities"]:
            ref, role = link.get("ref"), link.get("role")
            if ref not in entities:
                err(f"{path}: 实体引用不存在: {ref}")
            if role not in ROLES:
                err(f"{path}: role 非法: {role}")

        if not d["claims"]:
            err(f"{path}: claims 不能为空")
        for c in d["claims"]:
            n_claims += 1
            if "statement" not in c:
                err(f"{path}: claim 缺 statement")
            if c.get("confidence") not in (None, "reported", "verified", "inferred"):
                err(f"{path}: confidence 非法: {c.get('confidence')}")
            for m in c.get("metrics", []):
                n_metrics += 1
                if "value" not in m:
                    err(f"{path}: metric 缺 value: {m}")
                if m.get("ref") is not None and m["ref"] not in entities:
                    err(f"{path}: 指标引用不存在: {m['ref']}")
                if m.get("ref") is None and not m.get("name"):
                    err(f"{path}: 指标既无 ref 也无 name: {m}")

        for rel in d.get("relations", []):
            if rel.get("type") not in RELATION_TYPES:
                err(f"{path}: relation type 非法: {rel.get('type')}")
            if rel.get("ref") not in items:
                err(f"{path}: relation 引用的信息项不存在: {rel.get('ref')}")

        s = d["summaries"]
        if not s.get("one_liner_zh"):
            err(f"{path}: summaries.one_liner_zh 缺失")
        dd = s.get("deep_dive")
        if dd and not (ROOT / dd).exists():
            err(f"{path}: deep_dive 路径不存在: {dd}")

        a = d["assessment"]
        if a.get("relevance") not in RELEVANCE or a.get("decision") not in DECISIONS:
            err(f"{path}: assessment 枚举非法: {a.get('relevance')}/{a.get('decision')}")

    # 实体的 proposed_in 应回指已存在的信息项
    for eid, (path, e) in entities.items():
        pi = e.get("proposed_in")
        if pi and pi not in items:
            err(f"{path} {eid}: proposed_in 引用的信息项不存在: {pi}")

    # ---------- 报告 ----------
    by_type: dict[str, int] = {}
    for _, (_, e) in entities.items():
        by_type[e["type"]] = by_type.get(e["type"], 0) + 1
    print(f"实体 {len(entities)} 个: " + ", ".join(f"{k}={v}" for k, v in sorted(by_type.items())))
    print(f"信息项 {len(items)} 个, 论断 {n_claims} 条, 量化指标 {n_metrics} 处")
    for w in warnings:
        print(f"  [warn] {w}")
    if errors:
        print(f"\n✗ {len(errors)} 个错误:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("✓ kb 校验通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
