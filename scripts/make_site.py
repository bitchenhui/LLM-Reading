#!/usr/bin/env python3
"""站点生成器 v3：两页式前端（用户定义的形态）。

- 页签一「本周新成果」：最近 7 天新条目，按八大类分组
- 页签二「知识库」：领域问答（本地 serve.py 提供 /api/ask）+ 八大类领域综述
  （kb/synthesis/*.md，glm-5.3 基于全量条目合成的"发展历程/技术主线/关键问题"）

纯静态站点；重新生成：uv run --with pyyaml python scripts/make_site.py
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
from pathlib import Path

import yaml

from site_details import detail_url, write_details
from site_retest import write_sheets

ROOT = Path(__file__).resolve().parent.parent
ITEMS = ROOT / "kb" / "items"
SYNTH = ROOT / "kb" / "synthesis"
SITE = ROOT / "site"
REPO_URL = "https://github.com/bitchenhui/LLM-Reading"

DOMAIN_NAMES = {
    "video_image_coding": "视频/图像编码",
    "audio_coding": "音频编码",
    "streaming_delivery": "流媒体传输",
    "quality_assessment": "质量评估",
    "processing_enhancement": "处理增强",
    "immersive_media": "沉浸式·三维",
    "standards_ecosystem": "标准生态",
    "self_improvement": "AI 自我改进",
}
DOMAIN_ORDER = list(DOMAIN_NAMES)
CORE = "video_image_coding"
WEEK_DAYS = 7


def load(p: Path):
    return yaml.safe_load(p.read_text(encoding="utf-8"))


def entity_display_names() -> dict[str, str]:
    """实体 id → 人类可读名（优先中文别名，回退规范名）。"""
    out = {}
    for p in sorted((ROOT / "kb" / "entities").glob("*.yaml")):
        for e in load(p):
            zh = next((a for a in e.get("aliases", [])
                       if any("\u4e00" <= c <= "\u9fff" for c in a)), None)
            out[e["id"]] = zh or e["name"]
    return out


def build_graph(items: list[dict], min_count: int = 3) -> dict:
    """实体共现图：节点=实体（挂接≥min_count），边=同条目共现。python 侧力导向布局。"""
    import math
    import random

    linked: dict[str, int] = {}
    cooc: dict[tuple, int] = {}
    for d in items:
        refs = sorted({e["ref"] for e in d.get("entities", [])})
        for r in refs:
            linked[r] = linked.get(r, 0) + 1
        for i, a in enumerate(refs):
            for b in refs[i + 1:]:
                cooc[(a, b)] = cooc.get((a, b), 0) + 1

    keep = {e for e, c in linked.items() if c >= min_count}
    edges = [(a, b, w) for (a, b), w in cooc.items() if a in keep and b in keep and w >= 2]
    edges.sort(key=lambda x: -x[2])
    edges = edges[:240]
    nodes = sorted(keep)
    names = entity_display_names()

    # 力导向布局（确定性）
    random.seed(7)
    W, H = 880, 620
    pos = {n: [W / 2 + 260 * math.cos(i / max(1, len(nodes)) * 2 * math.pi),
               H / 2 + 200 * math.sin(i / max(1, len(nodes)) * 2 * math.pi)] for i, n in enumerate(nodes)}
    adj = defaultdict(dict)
    for a, b, w in edges:
        adj[a][b] = w
        adj[b][a] = w
    for _ in range(300):
        disp = {n: [0.0, 0.0] for n in nodes}
        for i, a in enumerate(nodes):
            for b in nodes[i + 1:]:
                dx, dy = pos[a][0] - pos[b][0], pos[a][1] - pos[b][1]
                d2 = dx * dx + dy * dy or 1.0
                f = 22000.0 / d2
                dx, dy = dx / math.sqrt(d2), dy / math.sqrt(d2)
                disp[a][0] += dx * f; disp[a][1] += dy * f
                disp[b][0] -= dx * f; disp[b][1] -= dy * f
        for a, nbrs in adj.items():
            for b, w in nbrs.items():
                if a < b:
                    dx, dy = pos[b][0] - pos[a][0], pos[b][1] - pos[a][1]
                    dist = math.sqrt(dx * dx + dy * dy) or 1.0
                    f = (dist - max(30.0, 140 - w * 8)) * 0.02
                    dx, dy = dx / dist, dy / dist
                    disp[a][0] += dx * f; disp[a][1] += dy * f
                    disp[b][0] -= dx * f; disp[b][1] -= dy * f
        for n in nodes:
            disp[n][0] += (W / 2 - pos[n][0]) * 0.004
            disp[n][1] += (H / 2 - pos[n][1]) * 0.004
            m = math.sqrt(disp[n][0] ** 2 + disp[n][1] ** 2) or 1.0
            step = min(m, 6.0)
            pos[n][0] = max(30, min(W - 30, pos[n][0] + disp[n][0] / m * step))
            pos[n][1] = max(24, min(H - 24, pos[n][1] + disp[n][1] / m * step))

    type_color = {"codec": "#5b9dff", "impl": "#4cc38a", "concept": "#b18cff",
                  "metric": "#f5a623", "dataset": "#8b93a7", "org": "#e5534b"}
    return {
        "nodes": [{"id": n, "name": names.get(n, n), "type": n.split(":")[0],
                   "count": linked[n], "x": round(pos[n][0]), "y": round(pos[n][1])}
                  for n in nodes],
        "edges": [{"a": a, "b": b, "w": w} for a, b, w in edges],
        "colors": type_color,
    }


def build_data(items: list[dict], today: date) -> dict:
    week_start = (today - timedelta(days=WEEK_DAYS - 1)).isoformat()
    end = today.isoformat()
    all_items = []
    for d in items:
        deep = d["summaries"].get("deep_dive")
        all_items.append({
            "id": d["id"],
            "type": d["type"],
            "domain": d.get("domain") or CORE,
            "title": d.get("title_zh") or d["title"],
            "orig_title": d["title"] if d.get("title_zh") else "",
            "published": d["time"]["published"],
            "detail": detail_url(d["id"]),
            "entities": [e["ref"] for e in d["entities"]],
            "url": d["source"]["url"],
            "one_liner": d["summaries"].get("one_liner_zh", ""),
            "deep": f"{REPO_URL}/blob/main/{deep}" if deep else None,
        })

    week = [i for i in all_items if week_start <= i["published"] <= end]
    week.sort(key=lambda x: x["published"], reverse=True)
    by_domain = {}
    for i in week:
        by_domain.setdefault(i["domain"], []).append(i)

    # 全量条目按域分组（知识库页的领域卡片用）：核心域在前，域内按时间倒序
    all_sorted = sorted(all_items, key=lambda x: x["published"], reverse=True)
    items_by_domain = {}
    for i in all_sorted:
        items_by_domain.setdefault(i["domain"], []).append(i)

    synthesis = {}
    if SYNTH.exists():
        for p in sorted(SYNTH.glob("*.md")):
            synthesis[p.stem] = p.read_text(encoding="utf-8")

    # 实体档案层：头部一行含名称与统计，卡片直接用
    dossiers = []
    doss_dir = ROOT / "kb" / "dossiers"
    if doss_dir.exists():
        for p in sorted(doss_dir.glob("*.md")):
            text = p.read_text(encoding="utf-8")
            first = text.split("\n", 1)[0].lstrip("# ").strip()
            sub = text.split("\n")[2][:60] if len(text.split("\n")) > 2 else ""
            dossiers.append({"id": p.stem, "title": first, "meta": sub, "md": text})

    # 时间线事实层（近 180 天）
    timeline = []
    tl_path = ROOT / "kb" / "timeline.yaml"
    if tl_path.exists():
        tdata = load(tl_path)
        ents_map = entity_display_names()
        timeline_start = (today - timedelta(days=179)).isoformat()
        timeline = [f for f in (tdata.get("facts") or []) if timeline_start <= f.get("date", "") <= end][:300]
        for f in timeline:
            f["entity_name"] = ents_map.get(f["entity"], f["entity"])

    # 调研报告 / SOTA 追踪 / 知识图谱
    reports = []
    rep_dir = ROOT / "docs" / "reports"
    if rep_dir.exists():
        for p in sorted(rep_dir.glob("*.md"), reverse=True):
            text = p.read_text(encoding="utf-8")
            title = next((l.lstrip("# ").strip() for l in text.split("\n") if l.startswith("# ")),
                         p.stem)
            first_para = next((l for l in text.split("\n") if l.strip() and not l.startswith("#")
                               and not l.startswith(">")), "")[:80]
            reports.append({"title": title, "sub": first_para, "md": text})
    sota = []
    sota_path = ROOT / "kb" / "sota.yaml"
    if sota_path.exists():
        sota = (load(sota_path).get("groups") or [])[:12]
    graph = build_graph(items)
    aliases = {}
    for p in sorted((ROOT / "kb" / "entities").glob("*.yaml")):
        for e in load(p):
            aliases[e["id"]] = " ".join(filter(None, [e["name"], e.get("full_name"), *e.get("aliases", [])]))

    return {
        "generated": end,
        "cutoff": week_start,
        "aliases": aliases,
        "repo_url": REPO_URL,
        "domain_names": DOMAIN_NAMES,
        "domain_order": DOMAIN_ORDER,
        "core": CORE,
        "stats": {
            "total": len(all_items),
            "week": len(week),
            "collected": sum(week_start <= d["time"]["collected"] <= end for d in items),
            "domains": {k: sum(1 for i in all_items if i["domain"] == k)
                        for k in DOMAIN_ORDER},
        },
        "week_by_domain": {k: by_domain.get(k, []) for k in
                           [CORE] + [d for d in DOMAIN_ORDER if d != CORE]},
        "items_by_domain": {k: items_by_domain.get(k, []) for k in
                            [CORE] + [d for d in DOMAIN_ORDER if d != CORE]},
        "synthesis": synthesis,
        "dossiers": dossiers,
        "timeline": timeline,
        "reports": reports,
        "sota": sota,
        "graph": graph,
    }


TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>音视频信息引擎</title>
<style>
:root {
  --bg: #0f1115; --panel: #171a21; --card: #1c2029; --border: #2a3040;
  --text: #e4e7ee; --dim: #98a1b3; --accent: #5b9dff; --green: #4cc38a;
  --orange: #f5a623; --purple: #b18cff;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: var(--bg); color: var(--text);
  font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif; line-height: 1.65; }
.wrap { max-width: 900px; margin: 0 auto; padding: 28px 20px 80px; }
header h1 { font-size: 21px; }
header .sub { color: var(--dim); font-size: 13px; margin-top: 3px; }
.tabs[hidden] { display:none; }
.tabs { display: flex; gap: 8px; margin: 18px 0 16px; }
.tab { border: 1px solid var(--border); background: var(--panel); color: var(--dim);
  border-radius: 10px; padding: 8px 18px; font-size: 14px; cursor: pointer; }
.tab.on { background: var(--accent); border-color: var(--accent); color: #fff; font-weight: 600; }
.note { font-size: 12.5px; color: var(--dim); margin-bottom: 14px; }
h2.sec { font-size: 16px; margin: 22px 0 10px; display: flex; align-items: baseline; gap: 8px; }
h2.sec .n { color: var(--dim); font-size: 13px; font-weight: 400; }
h2.sec .core-tag { font-size: 11px; color: var(--green); border: 1px solid var(--green);
  border-radius: 4px; padding: 0 5px; }
.item { background: var(--card); border: 1px solid var(--border); border-radius: 10px;
  padding: 12px 16px; margin-bottom: 10px; }
.item.read { border-left: 3px solid var(--green); }
.meta { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; font-size: 12px; color: #a4acbd; }
.badge { padding: 1px 8px; border-radius: 6px; font-size: 11.5px; font-weight: 600; }
.b-read { background: rgba(76,195,138,.15); color: var(--green); }
.b-rel { background: rgba(91,157,255,.12); color: #9db8e0; }
.item h3 { font-size: 14.5px; font-weight: 600; margin-top: 2px; }
.item h3 a { color: var(--text); text-decoration: none; }
.item h3 a:hover { color: var(--accent); }
.oneliner { font-size: 13px; color: #c6cdbe; margin-top: 3px; }
.links { margin-top: 6px; font-size: 12px; }
.links a { color: var(--accent); text-decoration: none; margin-right: 12px; }
.empty { color: var(--dim); font-size: 13px; text-align: center; padding: 40px 0; }
/* 知识库页 */
.qa { background: var(--panel); border: 1px solid var(--border); border-radius: 12px;
  padding: 16px 18px; margin-bottom: 20px; }
.qa .hint { font-size: 12.5px; color: var(--dim); margin-bottom: 10px; }
.qa .row { display: flex; gap: 10px; }
.qa input { flex: 1; background: var(--card); border: 1px solid var(--border); color: var(--text);
  border-radius: 8px; padding: 9px 12px; font-size: 14px; }
.qa button { background: var(--accent); border: none; color: #fff; border-radius: 8px;
  padding: 9px 20px; font-size: 14px; cursor: pointer; }
.qa button:disabled { opacity: .5; cursor: wait; }
.ans { margin-top: 14px; font-size: 13.5px; white-space: pre-wrap; }
.ans .used { margin-top: 10px; font-size: 11.5px; color: var(--dim); border-top: 1px dashed var(--border); padding-top: 8px; }
.syn { background: var(--card); border: 1px solid var(--border); border-radius: 12px;
  margin-bottom: 12px; overflow: hidden; }
.syn > .head { padding: 12px 16px; cursor: pointer; display: flex;
  justify-content: space-between; align-items: center; }
.syn > .head h3 { font-size: 14.5px; }
.syn > .head .arrow { color: var(--dim); font-size: 12px; }
.syn .body { display: none; padding: 4px 18px 16px; border-top: 1px solid var(--border);
  font-size: 13.5px; }
.syn.open .body { display: block; }
.row-item { padding: 8px 0; border-bottom: 1px dashed var(--border); }
.row-item:last-child { border-bottom: none; }
.row-item .l1 { display: flex; gap: 8px; align-items: baseline; flex-wrap: wrap; }
.row-item .d { color: #a4acbd; font-size: 11.5px; }
.row-item a { color: var(--text); text-decoration: none; font-size: 13.5px; font-weight: 600; }
.row-item a:hover { color: var(--accent); }
.row-item .ol { color: #c6cdbe; font-size: 12.5px; margin-top: 1px; }
.more-btn { display: inline-block; margin-top: 8px; color: var(--accent); font-size: 12.5px;
  cursor: pointer; user-select: none; }
.divider { margin: 14px 0 4px; font-size: 13px; color: var(--accent); font-weight: 600; }
.body h1 { font-size: 16px; margin: 12px 0 6px; }
.body h2 { font-size: 14.5px; margin: 14px 0 6px; color: var(--accent); }
.body h3 { font-size: 13.5px; margin: 10px 0 4px; }
.body p { margin: 6px 0; }
.body ul, .body ol { margin: 6px 0 6px 20px; }
.body code { background: var(--panel); border-radius: 4px; padding: 1px 5px; font-size: 12px; }
.body table { border-collapse: collapse; margin: 8px 0; font-size: 12.5px; }
.body th, .body td { border: 1px solid var(--border); padding: 4px 8px; }
.search { margin: 16px 0; }
.search label { display:block; margin-bottom:6px; font-weight:600; }
.search input { min-width:0; }
#searchResults a,.body table a { color:var(--accent); }
footer { color: var(--dim); font-size: 12px; margin-top: 36px; text-align: center; }
footer a { color: var(--dim); }
</style>
</head>
<body>
<div class="wrap">
<header>
  <h1>音视频信息引擎</h1>
  <div class="sub">8 个技术方向 · 论文与版本动态自动追踪 · AI 审阅精读 · 知识库问答</div>
</header>
<form class="qa search" role="search" method="get">
  <label for="searchQuery">站内搜索</label>
  <div class="row"><input id="searchQuery" name="q" type="search" placeholder="搜索标题、实体或关键词，如 VVenC" required>
  <button>搜索</button></div>
</form>
<div id="searchResults" hidden></div>
<div class="tabs">
  <button class="tab on" id="tab-week" onclick="showTab('week')">近七日发表</button>
  <button class="tab" id="tab-kb" onclick="showTab('kb')">知识库 · 问答</button>
</div>

<div id="view-week">
  <div class="note" id="weekNote"></div>
  <div id="weekList"></div>
</div>

<div id="view-kb" style="display:none">
  <div class="qa">
    <div class="hint">基于 8 大类知识库回答（引用条目 id，无据处会标注）。
      线上静态版不能携带密钥——问答需本地运行：<code>uv run --with pyyaml python scripts/serve.py</code> 后访问 127.0.0.1:8931</div>
    <div class="row">
      <input id="q" placeholder="例如：跨平台 NPU 部署的神经视频编码做到什么水平了？"
             onkeydown="if(event.key==='Enter')ask()">
      <button id="askBtn" onclick="ask()">提问</button>
    </div>
    <div class="ans" id="ans"></div>
  </div>
  <div class="note">八大类领域综述（发展历程 · 技术主线 · 关键问题），由引擎基于全量条目合成：</div>
  <div id="synList"></div>
  <div class="note" style="margin-top:22px">关键实体档案（"关于 X 我们都知道什么"，随数据滚动更新）：</div>
  <div id="dossList"></div>
  <div class="note" style="margin-top:22px">技术时间线（近 180 天：版本发布 · 高相关研究 · 标准提案；点击实体名过滤）：</div>
  <div id="tlList"></div>
  <div class="note" style="margin-top:22px">实验成绩（按数据集与锚点浏览，仅在实验条件一致时标注最优）</div>
  <div id="sotaList"></div>
  <div class="note" style="margin-top:22px">知识图谱（实体共现；节点大小=挂接条目数，颜色=类型；点击节点过滤时间线）：</div>
  <div id="graphBox"></div>
  <div class="note" style="margin-top:22px">调研报告（Deep Research：主题→全引用长文）：</div>
  <div id="repList"></div>
</div>

<footer id="foot"></footer>
</div>
<script>
const DATA = __DATA__;
const DN = DATA.domain_names;

document.getElementById("weekNote").innerHTML =
  `近七日（${DATA.cutoff} 至 ${DATA.generated}）发表 <b>${DATA.stats.week}</b> 条 · 同期收录 ${DATA.stats.collected} 条 · 累计 ${DATA.stats.total} 条`;

function badge(it) {
  let b = it.type === "repo_release" ? '<span class="badge b-rel">版本动态</span>'
    : (it.deep ? '<span class="badge b-read">已精读</span>' : "");
  return b;
}
function itemHTML(it) {
  const links = [`<a href="${it.url}" target="_blank">原文 ↗</a>`]
    .concat(it.deep ? [`<a href="${it.deep}" target="_blank">精读笔记 ↗</a>`] : []).join("");
  return `<div class="item${it.deep ? " read" : ""}">
    <div class="meta"><span>${it.published}</span>${badge(it)}</div>
    <h3><a href="${it.detail}">${esc(it.title)}</a></h3>
    <div class="oneliner">${esc(it.one_liner)}</div>
    <div class="links">${links}</div>
  </div>`;
}

const wl = document.getElementById("weekList");
let html = "";
for (const [dom, items] of Object.entries(DATA.week_by_domain)) {
  if (!items.length) continue;
  html += `<h2 class="sec">${DN[dom]}
    ${dom === DATA.core ? '<span class="core-tag">核心域</span>' : ""}
    <span class="n">${items.length} 条</span></h2>`;
  html += items.map(itemHTML).join("");
}
wl.innerHTML = html || `<div class="empty">最近 7 天无发表条目（引擎每日 09:30 自动拉取）</div>`;

function esc(s){ return s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;"); }
function md2html(md) {
  const lines = md.split("\\n");
  let out = [], inList = null, tableRows = [];
  const flushList = () => { if (inList) { out.push(`</${inList}>`); inList = null; } };
  const flushTable = () => {
    if (!tableRows.length) return;
    const rows = tableRows.filter(r => !/^\\s*\\|?\\s*:?-+/.test(r));
    out.push("<table>" + rows.map((r, i) => {
      const cells = r.split("|").slice(1, -1).map(c => c.trim());
      const tag = i === 0 ? "th" : "td";
      return "<tr>" + cells.map(c => `<${tag}>${inline(c)}</${tag}>`).join("") + "</tr>";
    }).join("") + "</table>");
    tableRows = [];
  };
  function inline(s) {
    return esc(s)
      .replace(/\\*\\*(.+?)\\*\\*/g, "<b>$1</b>")
      .replace(/`([^`]+)`/g, "<code>$1</code>");
  }
  for (const raw of lines) {
    const line = raw.trimEnd();
    if (line.trim().startsWith("|")) { flushList(); tableRows.push(line); continue; }
    flushTable();
    if (/^#{1,3}\\s/.test(line)) {
      flushList();
      const level = line.match(/^#+/)[0].length;
      out.push(`<h${level}>${inline(line.replace(/^#+\\s*/, ""))}</h${level}>`);
    } else if (/^[-*]\\s/.test(line)) {
      if (inList !== "ul") { flushList(); out.push("<ul>"); inList = "ul"; }
      out.push(`<li>${inline(line.replace(/^[-*]\\s*/, ""))}</li>`);
    } else if (/^\\d+\\.\\s/.test(line)) {
      if (inList !== "ol") { flushList(); out.push("<ol>"); inList = "ol"; }
      out.push(`<li>${inline(line.replace(/^\\d+\\.\\s*/, ""))}</li>`);
    } else if (line.trim() === "") {
      flushList();
    } else if (line.startsWith(">")) {
      flushList();
      out.push(`<p class="note">${inline(line.replace(/^>\\s*/, ""))}</p>`);
    } else {
      flushList();
      out.push(`<p>${inline(line)}</p>`);
    }
  }
  flushList(); flushTable();
  return out.join("");
}

function rowHTML(it, visible) {
  const links = [`<a href="${it.detail}">${esc(it.title)}</a>`]
    .concat(it.deep ? [`<a href="${it.deep}" target="_blank" style="font-weight:400;font-size:12px;color:var(--accent);">精读笔记↗</a>`] : []).join(" ");
  return `<div class="row-item"${visible ? "" : ' style="display:none"'}>
    <div class="l1"><span class="d">${it.published}</span>${badge(it)}${links}</div>
    <div class="ol">${esc(it.one_liner)}</div>
  </div>`;
}
window.showAll = (el, dom) => {
  document.getElementById("items-" + dom)
    .querySelectorAll(".row-item").forEach(r => r.style.display = "");
  el.remove();
};

const sl = document.getElementById("synList");
let synHTML = "";
for (const [dom, items] of Object.entries(DATA.items_by_domain)) {
  if (!items.length) continue;
  const md = DATA.synthesis[dom];
  const nPaper = items.filter(i => i.type === "paper").length;
  const nRel = items.filter(i => i.type === "repo_release").length;
  const counts = `论文 ${nPaper} · 版本动态 ${nRel}` + (md ? " · 附综述" : "");
  const itemsHTML = items.map((it, i) => rowHTML(it, i < 8)).join("") +
    (items.length > 8
      ? `<span class="more-btn" onclick="showAll(this, '${dom}')">显示全部 ${items.length} 条 ▼</span>` : "");
  synHTML += `<div class="syn" id="syn-${dom}">
    <div class="head" onclick="this.parentElement.classList.toggle('open')">
      <h3>${DN[dom] || dom}${dom === DATA.core ? ' <span class="core-tag" style="font-size:11px;color:var(--green);border:1px solid var(--green);border-radius:4px;padding:0 5px;">核心域</span>' : ""}</h3>
      <span class="arrow">${counts} · 展开/收起</span>
    </div>
    <div class="body">
      ${md ? md2html(md) + `<div class="divider">该领域全部条目（${items.length}）</div>` : ""}
      <div id="items-${dom}">${itemsHTML}</div>
    </div>
  </div>`;
}
sl.innerHTML = synHTML || '<div class="empty">领域综述生成中（scripts/synthesize_kb.py）</div>';

const dl = document.getElementById("dossList");
let dossHTML = "";
for (const d of DATA.dossiers) {
  dossHTML += `<div class="syn">
    <div class="head" onclick="this.parentElement.classList.toggle('open')">
      <h3>${d.title}</h3>
      <span class="arrow">${d.meta} · 展开/收起</span>
    </div>
    <div class="body">${md2html(d.md)}</div>
  </div>`;
}
dl.innerHTML = dossHTML || '<div class="empty">实体档案生成中（scripts/build_dossiers.py）</div>';

const KIND_ZH = { release: ["版本", "b-rel"], research: ["研究", "b-read"], standard: ["标准", "b-dom"] };
let tlEnt = "";
window.tlFilter = (name) => { tlEnt = (tlEnt === name ? "" : name); renderTL(); };
function renderTL() {
  const tl = document.getElementById("tlList");
  const facts = DATA.timeline.filter(f => !tlEnt || f.entity_name === tlEnt);
  let html = tlEnt ? `<div class="note">实体过滤：<b style="cursor:pointer" onclick="tlFilter('${tlEnt}')">${tlEnt} ✕</b>（${facts.length} 条）</div>` : "";
  let month = "";
  for (const f of facts) {
    if (f.date.slice(0, 7) !== month) {
      month = f.date.slice(0, 7);
      html += `<h2 class="sec">${month}<span class="n"></span></h2>`;
    }
    const k = KIND_ZH[f.kind] || [f.kind, "b-sum"];
    html += `<div class="row-item">
      <div class="l1"><span class="d">${f.date}</span>
        <span class="badge ${k[1]}">${k[0]}</span>
        <span class="ent" style="cursor:pointer" onclick="tlFilter('${f.entity_name}')">${f.entity_name}</span>
        ${f.url ? `<a href="${f.url}" target="_blank">${f.fact}</a>` : f.fact}</div>
    </div>`;
  }
  tl.innerHTML = html || '<div class="empty">该实体近期无时间线事实</div>';
}
renderTL();

// SOTA 追踪表
const sl2 = document.getElementById("sotaList");
let sotaHTML = "";
const itemById = new Map(Object.values(DATA.items_by_domain).flat().map(it => [it.id, it]));
const benchmark = new URLSearchParams(location.search).get("benchmark");
for (const g of DATA.sota) {
  const rows = g.entries.map(e => {
    const best = g.best != null && e.conditions && e.value === g.best;
    const c = e.conditions || {};
    const scope = [e.scope, c.dataset, c.anchor, c.setup, c.basis, c.statistic].filter(Boolean).join(" · ");
    const item = itemById.get(e.item);
    const method = item ? `<a href="${item.detail}">${esc(e.method)}</a>` : esc(e.method);
    const value = esc(String(e.value) + (c.unit || ""));
    const result = item && e.claim_id
      ? `<a href="${item.detail}/${encodeURIComponent(e.claim_id)}">${value}</a>` : value;
    const sheet = DATA.sheets[e.item]?.[e.claim_id];
    const retest = sheet ? `<br><a href="${sheet}">复测实验单</a>` : "";
    return `<tr><td>${e.date}</td><td>${method}<br><small>${esc(scope)}</small></td>
      <td>${result}${best ? " ★ 最优" : ""}${retest}</td></tr>`;
  }).join("");
  sotaHTML += `<div class="syn${benchmark === g.dataset ? " open" : ""}"><div class="head" onclick="this.parentElement.classList.toggle('open')">
    <h3>${esc(g.dataset)} × ${esc(g.anchor)}</h3>
    <span class="arrow">${esc(g.metric)} · ${g.n} 条 · ${g.best != null && g.entries.every(e => e.conditions) ? "同条件最优 " + g.best : "仅列结果"} · 展开/收起</span></div>
    <div class="body">
      <table style="width:100%"><tr><th>日期</th><th>方法</th><th>${esc(g.metric)}</th></tr>${rows}</table></div></div>`;
}
sl2.innerHTML = sotaHTML || '<div class="empty">SOTA 追踪生成中（scripts/build_sota.py）</div>';

// 知识图谱（python 预布局，SVG 渲染；点击节点过滤时间线）
const gp = DATA.graph;
if (gp && gp.nodes.length) {
  const pos = Object.fromEntries(gp.nodes.map(n => [n.id, n]));
  const edges = gp.edges.filter(e => pos[e.a] && pos[e.b]).map(e =>
    `<line x1="${pos[e.a].x}" y1="${pos[e.a].y}" x2="${pos[e.b].x}" y2="${pos[e.b].y}"
      stroke="#2a3040" stroke-opacity="${Math.min(0.15 + e.w * 0.08, 0.6)}" stroke-width="${Math.min(1 + e.w * 0.3, 3)}"/>`).join("");
  const maxC = Math.max(...gp.nodes.map(n => n.count));
  const nodes = gp.nodes.map(n => {
    const r = 4 + 14 * Math.sqrt(n.count / maxC);
    const color = gp.colors[n.type] || "#8b93a7";
    const label = n.count >= maxC * 0.15
      ? `<text x="${n.x}" y="${n.y - r - 4}" text-anchor="middle" fill="#c6cdbe" font-size="${Math.min(11, 8 + r / 3)}">${n.name}</text>` : "";
    return `<g data-n="${n.name}" style="cursor:pointer" onclick="tlFilter(this.dataset.n)">
      <circle cx="${n.x}" cy="${n.y}" r="${r}" fill="${color}" fill-opacity="0.85" stroke="#0f1115"><title>${n.name} · ${n.count} 条</title></circle>${label}</g>`;
  }).join("");
  document.getElementById("graphBox").innerHTML =
    `<svg viewBox="0 0 880 620" style="width:100%;background:var(--panel);border:1px solid var(--border);border-radius:12px">
     ${edges}${nodes}</svg>`;
} else {
  document.getElementById("graphBox").innerHTML = '<div class="empty">图谱数据不足</div>';
}

// 调研报告
const rl = document.getElementById("repList");
let repHTML = "";
for (const r of DATA.reports) {
  repHTML += `<div class="syn"><div class="head" onclick="this.parentElement.classList.toggle('open')">
    <h3>${r.title}</h3><span class="arrow">${r.sub}… · 展开/收起</span></div>
    <div class="body">${md2html(r.md)}</div></div>`;
}
rl.innerHTML = repHTML || '<div class="empty">尚无调研报告（scripts/research_report.py "主题"）</div>';

const query = (new URLSearchParams(location.search).get("q") || "").trim();
if (query) {
  document.getElementById("searchQuery").value = query;
  const terms = query.toLowerCase().split(/\\s+/);
  const matches = [];
  for (const item of Object.values(DATA.items_by_domain).flat()) {
    const title = [item.title, item.orig_title, item.id].join(" ").toLowerCase();
    const entities = item.entities.map(id => id + " " + (DATA.aliases[id] || "")).join(" ").toLowerCase();
    const summary = item.one_liner.toLowerCase();
    const scores = terms.map(t => title.includes(t) ? 8 : entities.includes(t) ? 3 : summary.includes(t) ? 1 : 0);
    if (scores.every(Boolean)) matches.push({item, score: scores.reduce((a,b) => a+b, 0)});
  }
  matches.sort((a,b) => b.score - a.score || Number(!!b.item.deep) - Number(!!a.item.deep)
    || b.item.published.localeCompare(a.item.published));
  const results = document.getElementById("searchResults");
  results.hidden = false;
  results.innerHTML = '<h2 class="sec">搜索结果 · ' + matches.length + ' 条</h2>'
    + '<p class="note"><a href="index.html">返回首页</a></p><div id="hits"></div>';
  let shown = 0;
  const more = document.createElement("button");
  more.className = "tab";
  more.textContent = "更多结果";
  function nextPage() {
    const page = matches.slice(shown, shown + 20);
    document.getElementById("hits").insertAdjacentHTML("beforeend", page.map(hit => rowHTML(hit.item, true)).join(""));
    shown += page.length;
    more.hidden = shown >= matches.length;
  }
  results.append(more);
  more.onclick = nextPage;
  nextPage();
  document.querySelector(".tabs").hidden = true;
  document.getElementById("view-week").hidden = true;
}

function showTab(t) {
  document.getElementById("view-week").style.display = t === "week" ? "" : "none";
  document.getElementById("view-kb").style.display = t === "kb" ? "" : "none";
  document.getElementById("tab-week").classList.toggle("on", t === "week");
  document.getElementById("tab-kb").classList.toggle("on", t === "kb");
}

if (benchmark && !query) {
  const group = sl2.querySelector(".syn.open");
  if (group) {
    showTab("kb");
    group.scrollIntoView();
  }
}

async function ask() {
  const q = document.getElementById("q").value.trim();
  const btn = document.getElementById("askBtn");
  const ans = document.getElementById("ans");
  if (!q) return;
  btn.disabled = true;
  ans.textContent = "检索知识库并思考中…（glm-5.3，约 1-2 分钟）";
  try {
    const r = await fetch("/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: q }),
    });
    if (!r.ok) throw new Error("HTTP " + r.status);
    const d = await r.json();
    ans.innerHTML = md2html(d.answer) +
      `<div class="used">引用 ${d.used.length} 条：${d.used.join(" · ")}</div>`;
  } catch (e) {
    ans.innerHTML = `<b>问答服务不可达</b>（${e.message}）。线上静态页不带密钥——
      本地运行 <code>uv run --with pyyaml python scripts/serve.py</code> 后访问
      <code>http://127.0.0.1:8931</code> 即可提问；下方领域综述始终可读。`;
  } finally {
    btn.disabled = false;
  }
}

document.getElementById("foot").innerHTML =
  `音视频信息引擎 · 数据与代码：<a href="${DATA.repo_url}" target="_blank">LLM-Reading</a> · 每日 09:30 自动更新`;
</script>
</body>
</html>
"""


def main() -> int:
    items = [load(p) for p in sorted(ITEMS.glob("*/*.yaml"))]
    data = build_data(items, datetime.now(ZoneInfo("Asia/Shanghai")).date())
    write_details(items, SITE, REPO_URL)
    data["sheets"] = write_sheets(items, SITE)
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = TEMPLATE.replace("__DATA__", payload)
    SITE.mkdir(exist_ok=True)
    out = SITE / "index.html"
    out.write_text(html, encoding="utf-8")
    n_synth = len(data["synthesis"])
    print(f"→ {out}（本周 {data['stats']['week']} 条，基底 {data['stats']['total']}，"
          f"综述 {n_synth} 篇，{len(html) // 1024} KB）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
