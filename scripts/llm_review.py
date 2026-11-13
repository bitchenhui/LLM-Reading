#!/usr/bin/env python3
"""LLM 审阅器：消费 queue/papers/ 的 pending 记录 → 精度终审 → 产出 kb items。

对应 kb/README.md 入库五步的 3-5 步：
  3. 精度终审（assessment：relevance/decision/reason）
  4. 提炼 claims（摘要可支撑的论断）+ 中文 summaries
  5. 落库 kb/items/papers/{id}.yaml，随后跑一致性校验

LLM 输出全部做词表裁剪与引用校验后才开始拼 item——模型说错枚举/编造实体时
降级处理而不是污染基底。decision=skip 的只回写队列状态，不落库。

用法：
  uv run --with pyyaml python scripts/llm_review.py --limit 5    # 先试跑几条看质量
  uv run --with pyyaml python scripts/llm_review.py              # 全量处理 pending
配置：config/llm.local.yaml（复制自 cc-switch Zhipu GLM，已 gitignore）
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
KB = ROOT / "kb"
QUEUE = ROOT / "queue" / "papers"
ITEMS = KB / "items" / "papers"
CONFIG = ROOT / "config" / "llm.local.yaml"

ROLES = ["subject", "uses", "builds_on", "evaluated_on", "measured_by",
         "compared_against", "affiliation", "platform"]
RELATION_TYPES = ["cites", "builds_on", "improves_on", "compares_with",
                  "same_topic", "complements", "contrasts_with"]
RESEARCH_LINES = ["traditional_codec_opt", "learned_codec", "coding_for_machines",
                  "generative_compression", "inr_representation", "systems_deployment"]
DOMAINS = ["video_image_coding", "audio_coding", "streaming_delivery",
           "quality_assessment", "processing_enhancement", "immersive_media",
           "standards_ecosystem", "self_improvement"]
CORE_DOMAIN = "video_image_coding"

INSTRUCTIONS = """你是音视频领域信息整合引擎的精度过滤器与初筛摘要器。
对给定论文完成四件事：判定领域大类（domain）、收录级别、中文初筛摘要、结构化论断。
只输出 JSON 本体，不要 markdown 代码块、不要解释。

领域大类（domain）：
- video_image_coding 视频/图像编码（核心域）
- audio_coding 音频/语音编码
- streaming_delivery 流媒体与传输（DASH/WebRTC/ABR/低延迟）
- quality_assessment 质量评估（IQA/VQA/QoE）
- processing_enhancement 编码链路处理与增强（超分/去噪/HDR/后滤波）
- immersive_media 沉浸式与三维（点云/NeRF/3DGS/光场）
- standards_ecosystem 标准进程/专利/许可
- self_improvement 自我改进 AI（RSI/EoH/FunSearch/AlphaEvolve/LLM agent 自改进）

收录基准：核心域（video_image_coding）可给 deep_read；其余域默认 summary_only
（重要工作最多 summary_only，不给 deep_read）。与音视频技术整体无关 → skip。"""

RELEASE_INSTRUCTIONS = """你是音视频/图像编码领域信息引擎的版本动态审阅器。
对开源编解码器仓库的 GitHub release 判定收录级别并写中文摘要。只输出 JSON 本体。

收录基准：有实质内容（性能/压缩率改进、新特性、标准适配、API 变化、工程里程碑）的
正式版与 rc → summary_only；重大版本（架构级变化、新标准支持）→ deep_read；
纯噪声（仅 CI/拼写/打包修复、无内容预发布）→ skip。"""


def build_prompt(rec: dict, entities: dict, known_items: list[tuple[str, str]]) -> str:
    meta = rec["meta"]
    matched = ", ".join(f"{m['ref']}(×{m['count']})" for m in rec.get("matched", [])) or "无"
    ent_list = "\n".join(f"  {eid}  [{entities[eid]['type']}]" for eid in
                         sorted({m["ref"] for m in rec.get("matched", [])} & entities.keys()))
    item_list = "\n".join(f"  {iid}  {title}" for iid, title in known_items) or "  （空）"
    return f"""论文元数据：
标题: {meta['title']}
作者: {', '.join(meta['authors'][:8])}
arXiv 分类: {', '.join(meta['categories'])}
摘要: {meta['abstract']}

规则阶段实体匹配（可能含噪声）: {matched}

可挂接实体（只能从下列中选择，剔除噪声匹配）:
{ent_list}

角色词表: subject=研究对象 uses=使用 builds_on=基于 evaluated_on=数据集 measured_by=指标 compared_against=对比锚点 affiliation=作者机构 platform=硬件平台
已有信息项（relations 只能引用下列 id，仅在确有联系时给）:
{item_list}

输出 JSON：
{{
 "domain": "video_image_coding|audio_coding|streaming_delivery|quality_assessment|processing_enhancement|immersive_media|standards_ecosystem|self_improvement",
 "decision": "deep_read|summary_only|skip",
 "relevance": "high|medium|low",
 "reason": "一句话中文理由",
 "title_zh": "中文标题",
 "one_liner_zh": "一句话总结（中文，≤60字）",
 "abstract_zh": "3-5句方法与结果中文摘要",
 "research_lines": [],
 "entities": [{{"ref": "…", "role": "…"}}],
 "claims": [{{"statement": "中文论断", "confidence": "reported", "metrics": [{{"name": "指标名", "value": "数值", "scope": "口径"}}]}}],
 "relations": [{{"type": "same_topic", "ref": "…", "note": "依据"}}]
}}
要求：entities 至少 1 条（subject 必须有）；claims 至少 1 条（摘要里有数字就带 metrics，
value 用字符串原样保留数值与单位，scope 写清锚点/条件；没有可靠数字就纯 statement）。"""


def build_release_prompt(rec: dict, entities: dict) -> str:
    meta = rec["meta"]
    ent_list = "\n".join(f"  {eid}  [{entities[eid]['type']}]" for eid in
                         sorted({m["ref"] for m in rec.get("matched", [])} & entities.keys()))
    notes = meta.get("notes") or "（无说明）"
    return f"""仓库: {meta['repo']}
版本: {meta['tag']}{'（预发布）' if meta.get('prerelease') else ''}
发布日期: {meta['published']}
Release 标题: {meta['name']}
Release 说明:
{notes}

可挂接实体（只能从下列中选择）:
{ent_list}

角色词表: subject=发布主体 uses=涉及的技术/概念/标准 measured_by=提及指标

输出 JSON：
{{
 "decision": "deep_read|summary_only|skip",
 "relevance": "high|medium|low",
 "reason": "一句话中文理由",
 "title_zh": "中文标题（如 VVenC 发布 v1.14.0）",
 "one_liner_zh": "一句话总结（中文，≤50字）",
 "abstract_zh": "2-3句版本要点中文摘要",
 "research_lines": [],
 "entities": [{{"ref": "…", "role": "subject"}}],
 "claims": [{{"statement": "版本要点论断", "confidence": "reported", "metrics": []}}],
 "relations": []
}}
claims 从 release notes 提取有信息量的要点（性能数字/新特性/兼容性变化）；
notes 无实质内容时 claims 只留一条「发布该版本」。"""


# ---------- LLM 客户端（Responses / chat-completions 自适应） ----------

class LLM:
    def __init__(self, cfg: dict):
        self.base = cfg["base_url"].rstrip("/")
        self.key = cfg["api_key"]
        self.models = cfg["models"]
        self.req = cfg.get("request", {})
        self.wire = cfg.get("wire", "responses")  # 先按配置的协议试
        self.usage = {"in": 0, "out": 0, "calls": 0}

    def chat(self, prompt: str, tier: str = "review", instructions: str | None = None,
             max_tokens: int | None = None) -> str:
        model = self.models[tier]
        max_tok = max_tokens or self.req.get("max_output_tokens", 4000)
        system = instructions if instructions is not None else INSTRUCTIONS
        payload = {"stream": True, "max_output_tokens": max_tok}
        if self.wire == "responses":
            payload.update({"model": model, "input": prompt, "instructions": system})
            effort = self.req.get(f"{tier}_reasoning")
            if effort:
                payload["reasoning"] = {"effort": effort}
            url = f"{self.base}/responses"
        else:
            payload.update({"model": model, "stream_options": {"include_usage": True},
                            "messages": [{"role": "system", "content": system},
                                         {"role": "user", "content": prompt}]})
            url = f"{self.base}/chat/completions"
        try:
            return self._post_stream(url, payload)
        except RuntimeError as e:
            if self.wire == "responses" and ("404" in str(e) or "400" in str(e)):
                print("    [wire] responses 不可用，切换 chat/completions", flush=True)
                self.wire = "chat"
                return self.chat(prompt, tier, instructions, max_tokens)
            raise

    def _post_stream(self, url: str, payload: dict) -> str:
        """SSE 流式：分块持续到达，避免长推理（深读 5-15 分钟）触发读超时。"""
        data = json.dumps(payload).encode()
        last = None
        for attempt in range(1, 4):
            try:
                req = urllib.request.Request(url, data=data, headers={
                    "Authorization": f"Bearer {self.key}",
                    "Content-Type": "application/json",
                    "Accept": "text/event-stream",
                })
                # timeout 是单次 read 的上限：SSE 心跳/增量会不断刷新它
                with urllib.request.urlopen(req, timeout=300) as resp:
                    parts: list[str] = []
                    usage: dict = {}
                    for raw in resp:
                        line = raw.decode("utf-8", errors="replace").strip()
                        if not line.startswith("data:"):
                            continue
                        body = line[5:].strip()
                        if body == "[DONE]":
                            break
                        try:
                            ev = json.loads(body)
                        except json.JSONDecodeError:
                            continue
                        if self.wire == "responses":
                            t = ev.get("type", "")
                            if t == "response.output_text.delta":
                                parts.append(ev.get("delta", ""))
                            elif t == "response.completed":
                                usage = (ev.get("response") or {}).get("usage") or usage
                        else:
                            if ev.get("usage"):
                                usage = ev["usage"]
                            for ch in ev.get("choices", []):
                                parts.append((ch.get("delta") or {}).get("content") or "")
                    self._track(usage)
                    out = "".join(parts)
                    if not out:
                        raise RuntimeError(f"流式响应无文本输出（wire={self.wire}）")
                    return out
            except urllib.error.HTTPError as e:
                body = e.read()[:300].decode(errors="replace")
                if e.code in (429, 500, 502, 503, 504):
                    wait = 20 * attempt
                    print(f"    [HTTP {e.code}] 退避 {wait}s", flush=True)
                    time.sleep(wait)
                    last = f"HTTP {e.code}: {body}"
                    continue
                raise RuntimeError(f"HTTP {e.code}: {body}") from e
            except Exception as e:  # noqa: BLE001
                wait = 15 * attempt
                print(f"    [流中断 {type(e).__name__}] 退避 {wait}s", flush=True)
                time.sleep(wait)
                last = repr(e)
        raise RuntimeError(f"流式重试耗尽: {last}")

    def _track(self, usage: dict | None) -> None:
        if usage:
            self.usage["in"] += usage.get("input_tokens") or usage.get("prompt_tokens") or 0
            self.usage["out"] += usage.get("output_tokens") or usage.get("completion_tokens") or 0
            self.usage["calls"] += 1


def parse_llm_json(text: str) -> dict:
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip())
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", text, re.S)  # 模型偶发前后缀说明，抠出最外层花括号
        if m:
            return json.loads(m.group(0))
        raise


# ---------- 裁剪与落库 ----------

# research_lines 的实体启发式：LLM 漏填时兜底（顺序即优先级，具体方向先于笼统方向）
LINE_MARKERS: list[tuple[str, set[str]]] = [
    ("coding_for_machines", {"concept:ICM"}),
    ("generative_compression", {"concept:DiffusionPrior", "concept:ConsistencySampling",
                                "concept:TrainingFree", "impl:CausalForcing", "impl:GLC-Video",
                                "impl:OneDC", "impl:WanVAE"}),
    ("inr_representation", {"concept:INR", "concept:FeatureGrid", "impl:HiNeRV", "impl:HiNeRV++",
                            "impl:NVRC", "impl:NVRC++", "impl:C3"}),
    ("systems_deployment", {"concept:NPU"}),
    ("learned_codec", {"impl:DCVC-RT", "impl:DCVC-FM", "impl:TIC", "impl:TinyLIC", "impl:TCM",
                       "concept:Hyperprior", "concept:EntropyModel", "impl:MoECodec"}),
    ("traditional_codec_opt", {"impl:VVenC", "impl:VTM", "impl:HM", "impl:x264", "impl:x265",
                               "impl:SVT-AV1", "impl:HEVC-QSV", "impl:VVdec", "impl:dav1d",
                               "impl:libavif", "impl:kvazaar", "concept:QP", "concept:RDO",
                               "concept:MMVD", "concept:LTR"}),
]


# 这些角色表达的是「对比锚点/机构/平台」，不能作为主线归类依据
NON_CLASSIFYING_ROLES = {"compared_against", "affiliation", "platform", "evaluated_on", "measured_by"}


def infer_research_lines(entity_links: list) -> list[str]:
    refs = {lk["ref"] for lk in entity_links
            if isinstance(lk, dict) and lk.get("role") not in NON_CLASSIFYING_ROLES}
    out = [line for line, markers in LINE_MARKERS if refs & markers]
    return out[:3]


# domain 的实体启发式：LLM 漏判/错判时的兜底
DOMAIN_MARKERS: list[tuple[str, set[str]]] = [
    ("self_improvement", {"concept:SelfImprovement", "concept:EoH", "concept:RSI",
                          "concept:FunSearch", "concept:AlphaEvolve"}),
    ("audio_coding", {"codec:IAMF", "codec:Opus", "codec:EVS", "codec:MPEG-H-Audio",
                      "concept:NeuralAudioCodec"}),
    ("immersive_media", {"concept:NeRF", "concept:3DGS", "codec:G-PCC", "codec:V-PCC",
                         "concept:VolumetricVideo"}),
    ("streaming_delivery", {"concept:DASH", "concept:WebRTC", "concept:ABR",
                            "concept:HLS", "concept:CMAF", "concept:QUIC"}),
    ("quality_assessment", {"concept:IQA", "concept:QoE"}),
    ("processing_enhancement", {"concept:SuperResolution"}),
    ("standards_ecosystem", {"org:Access-Advance", "org:Via-LA"}),
]


def infer_domain(entity_links: list) -> str:
    """subject 实体的归属优先（交叉方法论文：编码器主体→核心域，EoH 主体→self_improvement）；
    subject 不在标记集内时再按 uses 弱信号。"""
    subj = {lk["ref"] for lk in entity_links
            if isinstance(lk, dict) and lk.get("role") == "subject"}
    for domain, markers in DOMAIN_MARKERS:
        if subj & markers:
            return domain
    refs = {lk["ref"] for lk in entity_links
            if isinstance(lk, dict) and lk.get("role") not in NON_CLASSIFYING_ROLES}
    for domain, markers in DOMAIN_MARKERS:
        if refs & markers:
            return domain
    return CORE_DOMAIN


def sanitize(out: dict, rec: dict, entities: dict, known_ids: set[str], today: str) -> dict | None:
    """词表裁剪 + 引用校验。decision=skip 返回 None。"""
    decision = out.get("decision") if out.get("decision") in ("deep_read", "summary_only", "skip") else "summary_only"
    relevance = out.get("relevance") if out.get("relevance") in ("high", "medium", "low") else "medium"

    allowed = {m["ref"] for m in rec.get("matched", [])}
    ents = []
    for e in out.get("entities", []):
        if isinstance(e, dict) and e.get("ref") in allowed and e.get("role") in ROLES \
                and not any(x["ref"] == e["ref"] for x in ents):
            ents.append({"ref": e["ref"], "role": e["role"]})
    if ents and not any(e["role"] == "subject" for e in ents):
        ents[0] = {"ref": ents[0]["ref"], "role": "subject"}

    claims = []
    for c in out.get("claims", []):
        if not isinstance(c, dict) or not c.get("statement"):
            continue
        cl = {"statement": str(c["statement"]),
              "confidence": c.get("confidence") if c.get("confidence") in ("reported", "verified", "inferred") else "reported"}
        metrics = []
        for m in c.get("metrics", []):
            if isinstance(m, dict) and m.get("value") is not None and (m.get("name") or m.get("ref")):
                metrics.append({k: m[k] for k in ("ref", "name", "value", "unit", "scope") if m.get(k)})
        if metrics:
            cl["metrics"] = metrics
        cl["evidence"] = "abstract（初筛，未读全文）"
        claims.append(cl)

    rels = []
    for r in out.get("relations", []):
        if isinstance(r, dict) and r.get("ref") in known_ids and r.get("type") in RELATION_TYPES:
            rels.append({k: r[k] for k in ("type", "ref", "note") if r.get(k)})

    if decision == "skip" or not ents or not claims:
        return None

    rl = [l for l in out.get("research_lines", []) if l in RESEARCH_LINES]
    domain = out.get("domain") if out.get("domain") in DOMAINS else infer_domain(ents)
    if domain != CORE_DOMAIN and decision == "deep_read":
        decision = "summary_only"  # 非核心域降级：v1 只 summary 跟踪
    return {
        "decision": decision, "relevance": relevance,
        "domain": domain,
        "reason": str(out.get("reason", ""))[:200] or "（模型未给理由）",
        "title_zh": str(out.get("title_zh", "")) or None,
        "one_liner": str(out.get("one_liner_zh", "")) or None,
        "abstract_zh": str(out.get("abstract_zh", "")) or None,
        "research_lines": rl or infer_research_lines(ents) if domain == CORE_DOMAIN else [],
        "entities": ents, "claims": claims, "relations": rels,
    }


def build_item(rec: dict, s: dict, today: str, model: str) -> dict:
    meta = rec["meta"]
    arxiv_id = rec["id"].split(":")[-1]
    item = {
        "id": rec["id"],
        "type": "paper",
        "title": meta["title"],
        "domain": s["domain"],
        "research_lines": s["research_lines"],
        "source": {
            "channel": "arxiv",
            "external_id": arxiv_id + meta.get("version", ""),
            "url": meta["url"],
            "pdf_url": meta["pdf_url"],
            "venue": "arXiv preprint",
        },
        "time": {"published": meta["published"], "collected": today},
        "entities": s["entities"],
        "claims": s["claims"],
        "summaries": {"one_liner_zh": s["one_liner"], "abstract_zh": s["abstract_zh"]},
        "assessment": {
            "relevance": s["relevance"], "decision": s["decision"],
            "reason": s["reason"], "reviewer": f"{model}(llm_review)",
        },
        "provenance": {"created": today, "actor": "pipeline-v0", "pipeline": "llm_review"},
    }
    if s["title_zh"]:
        item["title_zh"] = s["title_zh"]
    if s["relations"]:
        item["relations"] = s["relations"]
    return item


def build_release_item(rec: dict, s: dict, today: str, model: str) -> dict:
    meta = rec["meta"]
    item = {
        "id": rec["id"],
        "type": "repo_release",
        "title": meta.get("name") or f"{meta['repo'].split('/')[-1]} {meta['tag']}",
        "domain": s["domain"],
        "research_lines": s["research_lines"],
        "source": {
            "channel": "github",
            "external_id": f"{meta['repo']}@{meta['tag']}",
            "url": meta["url"],
        },
        "time": {"published": meta.get("published") or today, "collected": today},
        "entities": s["entities"],
        "claims": s["claims"],
        "summaries": {"one_liner_zh": s["one_liner"], "abstract_zh": s["abstract_zh"]},
        "assessment": {
            "relevance": s["relevance"], "decision": s["decision"],
            "reason": s["reason"], "reviewer": f"{model}(llm_review)",
        },
        "provenance": {"created": today, "actor": "pipeline-v0", "pipeline": "llm_review"},
    }
    if s["title_zh"]:
        item["title_zh"] = s["title_zh"]
    return item


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="本次最多处理条数（0=全部）")
    ap.add_argument("--dry-run", action="store_true", help="只打印判定，不落库")
    ap.add_argument("--backfill-lines", action="store_true",
                    help="只为 research_lines 为空的存量 items 补实体启发式分类（无 LLM 调用）")
    ap.add_argument("--backfill-domain", action="store_true",
                    help="为缺 domain 的存量 items 补领域大类（实体启发式，无 LLM 调用）")
    args = ap.parse_args()

    if args.backfill_domain:
        n = 0
        for p in sorted((KB / "items").glob("*/*.yaml")):
            d = yaml.safe_load(open(p, encoding="utf-8"))
            if not d.get("domain"):
                d["domain"] = infer_domain(d.get("entities", []))
                yaml.safe_dump(d, open(p, "w", encoding="utf-8"),
                               allow_unicode=True, sort_keys=False, width=100)
                n += 1
        print(f"回填 domain {n} 条")
        return 0

    if args.backfill_lines:
        n = 0
        for p in sorted(ITEMS.glob("*.yaml")):
            d = yaml.safe_load(open(p, encoding="utf-8"))
            if not d.get("research_lines"):
                d["research_lines"] = infer_research_lines(d["entities"])
                if d["research_lines"]:
                    yaml.safe_dump(d, open(p, "w", encoding="utf-8"),
                                   allow_unicode=True, sort_keys=False, width=100)
                    n += 1
        print(f"回填 research_lines {n} 条")
        return 0

    cfg = yaml.safe_load(open(CONFIG, encoding="utf-8"))
    llm = LLM(cfg)
    entities: dict[str, dict] = {}
    for p in sorted((KB / "entities").glob("*.yaml")):
        for e in yaml.safe_load(open(p, encoding="utf-8")):
            entities[e["id"]] = e
    known_items = []
    for p in sorted((KB / "items").glob("*/*.yaml")):
        d = yaml.safe_load(open(p, encoding="utf-8"))
        known_items.append((d["id"], d["title"]))
    known_ids = {i for i, _ in known_items}

    pendings = []
    for p in sorted((ROOT / "queue").glob("*/*.yaml")):
        d = yaml.safe_load(open(p, encoding="utf-8"))
        if d.get("status") == "pending":
            d["_kind"] = d.get("kind", "paper") if p.parent.name == "repos" else "paper"
            pendings.append(d)
    pendings.sort(key=lambda d: -d.get("score", 0))
    if args.limit:
        pendings = pendings[: args.limit]
    print(f"pending 待审 {len(pendings)} 条（按规则分排序）\n")

    today = date.today().isoformat()
    n_item = n_skip = n_fail = 0
    for rec in pendings:
        is_release = rec["_kind"] == "release"
        label = rec["meta"]["repo"] + " " + rec["meta"]["tag"] if is_release \
            else rec["meta"]["title"][:60]
        print(f"[{rec['id'].split(':')[-1]}] score={rec.get('score')} {label}")
        try:
            if is_release:
                raw = llm.chat(build_release_prompt(rec, entities),
                               instructions=RELEASE_INSTRUCTIONS)
            else:
                raw = llm.chat(build_prompt(rec, entities, known_items))
            out = parse_llm_json(raw)
        except Exception as e:  # noqa: BLE001
            n_fail += 1
            print(f"    ✗ 调用/解析失败: {e}")
            continue
        s = sanitize(out, rec, entities, known_ids, today)
        stem = f"{rec['id'].split(':')[-1]}.yaml"
        qpath = (ROOT / "queue" / "repos" / stem) if is_release else (QUEUE / stem)
        out_dir = KB / "items" / ("releases" if is_release else "papers")
        out_dir.mkdir(parents=True, exist_ok=True)
        if s is None:
            n_skip += 1
            rec.pop("_kind", None)
            rec["status"] = "skipped_by_llm"
            rec["llm_decision"] = out.get("decision", "skip")
            rec["llm_reason"] = str(out.get("reason", ""))[:200]
            print(f"    → skip（{rec['llm_reason'][:50]}）")
            if not args.dry_run:
                yaml.safe_dump(rec, open(qpath, "w", encoding="utf-8"),
                               allow_unicode=True, sort_keys=False, width=100)
            continue
        n_item += 1
        if is_release:
            item = build_release_item(rec, s, today, llm.models["review"])
        else:
            item = build_item(rec, s, today, llm.models["review"])
        print(f"    → {s['decision']} / {s['relevance']}｜{s['one_liner'][:50]}")
        if not args.dry_run:
            yaml.safe_dump(item, open(out_dir / stem, "w", encoding="utf-8"),
                           allow_unicode=True, sort_keys=False, width=100)
            rec.pop("_kind", None)
            rec["status"] = "reviewed"
            rec["llm_decision"] = s["decision"]
            yaml.safe_dump(rec, open(qpath, "w", encoding="utf-8"),
                           allow_unicode=True, sort_keys=False, width=100)
            known_items.append((item["id"], item["title"]))
            known_ids.add(item["id"])

    print(f"\n产出 item {n_item}，LLM skip {n_skip}，失败 {n_fail}；"
          f"tokens in={llm.usage['in']} out={llm.usage['out']} calls={llm.usage['calls']}")

    if not args.dry_run and n_item:
        print("\n运行基底校验：")
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_kb.py")])
        return r.returncode
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
