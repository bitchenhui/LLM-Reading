#!/usr/bin/env python3
"""站点生成器（消费端 v2）：基底 → 自包含单页前端 site/index.html。

v2 设计原则（对着 v1 可用性评审改的）：
- 默认视图 = 核心域（视频/图像编码），不再让最新但非核心的条目霸屏
- 术语全部人话：已精读/摘要收录/版本动态；实体标签显示名称而非 concept: 前缀
- 渐进披露：卡片只留 标题+一句话+入口；论断/实体收进展开区
- 顶部一段话讲清这是什么 + 图例

零依赖、单文件；重新生成即更新：uv run --with pyyaml python scripts/make_site.py
"""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ITEMS = ROOT / "kb" / "items"
SITE = ROOT / "site"
REPO_URL = "https://github.com/bitchenhui/LLM-Reading"

LINE_NAMES = {
    "traditional_codec_opt": "传统编码器优化",
    "learned_codec": "学习式编码",
    "coding_for_machines": "面向机器视觉",
    "generative_compression": "生成式压缩",
    "inr_representation": "INR 表示压缩",
    "systems_deployment": "系统与部署",
}
DOMAIN_NAMES = {
    "video_image_coding": "视频/图像编码",
    "audio_coding": "音频编码",
    "streaming_delivery": "流媒体传输",
    "quality_assessment": "质量评估",
    "processing_enhancement": "处理增强",
    "immersive_media": "沉浸式·三维",
    "standards_ecosystem": "标准生态",
    "self_improvement": "自我改进 AI",
}
CORE = "video_image_coding"


def load(p: Path):
    return yaml.safe_load(open(p, encoding="utf-8"))


def entity_display_names() -> dict[str, str]:
    """实体 id → 人类可读名（优先中文别名，回退规范名）。"""
    out = {}
    for p in sorted((ROOT / "kb" / "entities").glob("*.yaml")):
        for e in load(p):
            zh = next((a for a in e.get("aliases", []) if any("\u4e00" <= c <= "\u9fff" for c in a)), None)
            out[e["id"]] = zh or e["name"]
    return out


def metric_text(m: dict) -> str:
    label = m.get("name") or m.get("ref", "").split(":")[-1]
    val = m.get("value", "")
    unit = m.get("unit", "")
    if isinstance(val, (int, float)):
        val = f"{val}{unit}" if unit else str(val)
    return f"{label} {val}" + (f"（{m.get('scope')}）" if m.get("scope") else "")


def build_data() -> dict:
    ents = entity_display_names()
    items = []
    for p in sorted(ITEMS.glob("*/*.yaml")):
        d = load(p)
        deep = d["summaries"].get("deep_dive")
        items.append({
            "id": d["id"],
            "type": d["type"],
            "domain": d.get("domain") or CORE,
            "title": d["title"],
            "title_zh": d.get("title_zh"),
            "published": d["time"]["published"],
            "collected": d["time"]["collected"],
            "url": d["source"]["url"],
            "lines": d.get("research_lines") or [],
            "relevance": d["assessment"]["relevance"],
            "decision": d["assessment"]["decision"],
            "one_liner": d["summaries"].get("one_liner_zh", ""),
            "claims": [
                {"statement": c["statement"],
                 "metrics": [metric_text(m) for m in c.get("metrics", [])]}
                for c in d.get("claims", [])
            ],
            "entities": [e["ref"] for e in d.get("entities", [])],
            "deep_dive_url": f"{REPO_URL}/blob/main/{deep}" if deep else None,
            "manual": d.get("provenance", {}).get("actor") == "manual-backfill",
        })
    items.sort(key=lambda x: x["published"], reverse=True)
    return {
        "generated": date.today().isoformat(),
        "repo_url": REPO_URL,
        "line_names": LINE_NAMES,
        "domain_names": DOMAIN_NAMES,
        "core": CORE,
        "entity_names": ents,
        "stats": {
            "papers": sum(1 for i in items if i["type"] == "paper"),
            "releases": sum(1 for i in items if i["type"] == "repo_release"),
            "claims": sum(len(i["claims"]) for i in items),
            "deep_reads": sum(1 for i in items if i["deep_dive_url"]),
        },
        "items": items,
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
  --text: #e4e7ee; --dim: #8b93a7; --accent: #5b9dff; --green: #4cc38a;
  --orange: #f5a623; --red: #e5534b; --purple: #b18cff;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: var(--bg); color: var(--text);
  font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif;
  line-height: 1.6; }
.wrap { max-width: 1080px; margin: 0 auto; padding: 28px 20px 80px; }
header h1 { font-size: 22px; }
header .sub { color: var(--dim); font-size: 13px; margin-top: 4px; }
.stats { display: flex; gap: 10px; margin: 16px 0 10px; flex-wrap: wrap; }
.stat { background: var(--panel); border: 1px solid var(--border); border-radius: 10px;
  padding: 8px 14px; font-size: 12.5px; color: var(--dim); }
.stat b { color: var(--text); font-size: 16px; margin-right: 3px; }
.legend { font-size: 12px; color: var(--dim); margin-bottom: 6px; }
.legend .b { margin: 0 2px; }
.filters { position: sticky; top: 0; background: var(--bg); padding: 10px 0;
  border-bottom: 1px solid var(--border); z-index: 5; }
.chips { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 8px; }
.chip { border: 1px solid var(--border); background: var(--panel); color: var(--dim);
  border-radius: 999px; padding: 3px 12px; font-size: 12.5px; cursor: pointer; user-select: none; }
.chip.on { background: var(--accent); border-color: var(--accent); color: #fff; }
.chips.sub { padding-left: 2px; }
.chips.sub .chip.on { background: rgba(91,157,255,.2); border-color: var(--accent); color: var(--accent); }
.row { display: flex; gap: 10px; flex-wrap: wrap; }
input[type=search], select { background: var(--panel); border: 1px solid var(--border);
  color: var(--text); border-radius: 8px; padding: 6px 10px; font-size: 13px; }
input[type=search] { flex: 1; min-width: 200px; }
.card { background: var(--card); border: 1px solid var(--border); border-radius: 12px;
  padding: 14px 18px; margin-bottom: 12px; }
.card.read { border-left: 3px solid var(--green); }
.card.top { border-left: 3px solid var(--accent); }
.meta { display: flex; gap: 6px; align-items: center; flex-wrap: wrap;
  font-size: 12px; color: #a4acbd; margin-bottom: 6px; }
.badge { padding: 1px 8px; border-radius: 6px; font-size: 11.5px; font-weight: 600; }
.b-read { background: rgba(76,195,138,.15); color: var(--green); }
.b-sum { background: rgba(177,140,255,.14); color: var(--purple); }
.b-rel { background: rgba(91,157,255,.12); color: #9db8e0; }
.b-dom { background: rgba(245,166,35,.13); color: var(--orange); }
.b-line { background: transparent; border: 1px solid var(--border); color: var(--dim); font-weight: 500; }
h3 { font-size: 15.5px; font-weight: 600; }
h3 a { color: var(--text); text-decoration: none; }
h3 a:hover { color: var(--accent); }
.orig { color: #a4acbd; font-size: 12px; margin-top: 1px; }
.oneliner { font-size: 13.5px; margin: 8px 0 2px; color: #c6cdbe; }
.actions { margin-top: 8px; display: flex; gap: 14px; font-size: 12.5px; align-items: baseline; }
.actions a { color: var(--accent); text-decoration: none; }
.actions .toggle { color: var(--accent); cursor: pointer; user-select: none; }
.detail { display: none; margin-top: 10px; border-top: 1px dashed var(--border); padding-top: 10px; }
.claim { font-size: 13px; margin-bottom: 8px; }
.claim .m { color: var(--green); font-size: 12.5px; margin-left: 6px; }
.ents { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 8px; }
.ents .lbl { font-size: 11.5px; color: var(--dim); margin-right: 2px; }
.ent { font-size: 11.5px; color: var(--dim); background: var(--panel);
  border: 1px solid var(--border); border-radius: 5px; padding: 1px 7px; cursor: pointer; }
.ent:hover { color: var(--accent); border-color: var(--accent); }
.empty { color: var(--dim); text-align: center; padding: 60px 0; }
footer { color: var(--dim); font-size: 12px; margin-top: 30px; text-align: center; }
footer a { color: var(--dim); }
</style>
</head>
<body>
<div class="wrap">
<header>
  <h1>音视频信息引擎</h1>
  <div class="sub">自动追踪 8 个技术方向的论文与开源编码器版本动态，AI 审阅精读后结构化入库 · 每日更新</div>
</header>
<div class="stats" id="stats"></div>
<div class="legend" id="legend"></div>
<div class="filters">
  <div class="chips" id="domChips"></div>
  <div class="chips sub" id="lineChips"></div>
  <div class="row">
    <input type="search" id="q" placeholder="搜索标题、摘要、论断内容…">
    <select id="kind">
      <option value="">全部内容</option>
      <option value="read">只看已精读</option>
      <option value="release">只看版本动态</option>
    </select>
    <select id="sort">
      <option value="new">最新优先</option>
      <option value="top">重点优先</option>
    </select>
  </div>
</div>
<div id="list"></div>
<div class="empty" id="empty" style="display:none">无匹配条目</div>
<footer id="foot"></footer>
</div>
<script>
const DATA = __DATA__;
const LINE = DATA.line_names, DOMAIN = DATA.domain_names, ENT = DATA.entity_names;
const REL_RANK = { high: 0, medium: 1, low: 2 };
const state = { dom: DATA.core, lines: new Set(), q: "", kind: "", sort: "new", ent: "" };

document.getElementById("stats").innerHTML =
  `<div class="stat"><b>${DATA.stats.papers}</b>篇论文</div>` +
  `<div class="stat"><b>${DATA.stats.releases}</b>条版本动态</div>` +
  `<div class="stat"><b>${DATA.stats.claims}</b>条关键论断</div>` +
  `<div class="stat"><b>${DATA.stats.deep_reads}</b>篇精读笔记</div>` +
  `<div class="stat">更新 ${DATA.generated}</div>`;
document.getElementById("legend").innerHTML =
  `<span class="badge b-read">已精读</span> 附全文精读笔记　` +
  `<span class="badge b-sum">摘要收录</span> 结构化摘要（未读全文）　` +
  `<span class="badge b-rel">版本动态</span> 开源编码器发布　` +
  `<span class="badge b-dom">橙标</span> 非编码大类`;

// 大类 pills（核心域默认选中）
const domChips = document.getElementById("domChips");
function chip(label, on, onclick) {
  const el = document.createElement("span");
  el.className = "chip" + (on ? " on" : ""); el.textContent = label;
  el.onclick = onclick; return el;
}
domChips.appendChild(chip("全部大类", false, () => { setDom(""); }));
for (const [k, name] of Object.entries(DOMAIN)) {
  const n = DATA.items.filter(i => i.domain === k).length;
  if (!n) continue;  // 0 计数大类不显示
  const short = k === "self_improvement" ? "AI 自我改进" : name;
  const el = chip(`${short} ${n}`, state.dom === k, () => setDom(k === state.dom ? "" : k));
  el.dataset.k = k; domChips.appendChild(el);
}
function setDom(k) {
  state.dom = k; state.lines.clear();
  document.querySelectorAll("#domChips .chip").forEach(c => {
    c.classList.toggle("on", c.dataset.k ? c.dataset.k === k : k === "");
  });
  renderLines(); render();
}

// 编码域细分主线（仅核心域视图下显示）
const lineChips = document.getElementById("lineChips");
function renderLines() {
  lineChips.innerHTML = "";
  if (state.dom !== DATA.core) return;
  const all = chip("全部主线", state.lines.size === 0, () => { state.lines.clear(); renderLines(); render(); });
  lineChips.appendChild(all);
  for (const [k, name] of Object.entries(LINE)) {
    const n = DATA.items.filter(i => i.domain === DATA.core && i.lines.includes(k)).length;
    if (!n) continue;
    const el = chip(`${name} ${n}`, state.lines.has(k), () => {
      state.lines.has(k) ? state.lines.delete(k) : state.lines.add(k);
      renderLines(); render();
    });
    lineChips.appendChild(el);
  }
}

document.getElementById("q").oninput = e => { state.q = e.target.value.toLowerCase(); render(); };
document.getElementById("kind").onchange = e => { state.kind = e.target.value; render(); };
document.getElementById("sort").onchange = e => { state.sort = e.target.value; render(); };
window.filterEnt = ref => { state.ent = state.ent === ref ? "" : ref; render(); };
window.toggleDetail = el => {
  const d = el.closest(".card").querySelector(".detail");
  const open = d.style.display === "block";
  d.style.display = open ? "none" : "block";
  el.textContent = open ? "收起论断 ▲" : "展开论断（" + el.dataset.n + "）▼";
};

function match(it) {
  if (state.dom && it.domain !== state.dom) return false;
  if (state.lines.size && !it.lines.some(l => state.lines.has(l))) return false;
  if (state.kind === "read" && !(it.deep_dive_url)) return false;
  if (state.kind === "release" && it.type !== "repo_release") return false;
  if (state.ent && !it.entities.includes(state.ent)) return false;
  if (state.q) {
    const hay = (it.title + " " + (it.title_zh || "") + " " + it.one_liner + " " +
      it.claims.map(c => c.statement).join(" ") + " " +
      it.entities.map(e => ENT[e] || e).join(" ")).toLowerCase();
    if (!hay.includes(state.q)) return false;
  }
  return true;
}

function card(it) {
  const isRel = it.type === "repo_release";
  const badges =
    (isRel
      ? '<span class="badge b-rel">版本动态</span>' +
        (it.deep_dive_url ? '<span class="badge b-read">已精读</span>' : "")
      : (it.domain !== DATA.core ? `<span class="badge b-dom">${DOMAIN[it.domain]}</span>` : "") +
        (it.deep_dive_url ? '<span class="badge b-read">已精读</span>' : '<span class="badge b-sum">摘要收录</span>'));
  const lines = it.domain === DATA.core && it.lines.length
    ? it.lines.map(l => `<span class="badge b-line">${LINE[l]}</span>`).join("") : "";
  const claims = it.claims.map(c => {
    const m = c.metrics.map(x => `<span class="m">▸ ${x}</span>`).join(" ");
    return `<div class="claim">· ${c.statement}${m}</div>`;
  }).join("");
  const ents = it.entities.slice(0, 10).map(e =>
    `<span class="ent" onclick="filterEnt('${e}')">${ENT[e] || e}</span>`).join("");
  const links = [`<a href="${it.url}" target="_blank">原文 ↗</a>`]
    .concat(it.deep_dive_url ? [`<a href="${it.deep_dive_url}" target="_blank">精读笔记 ↗</a>`] : [])
    .join("");
  const cls = it.deep_dive_url ? "card read" : (it.relevance === "high" ? "card top" : "card");
  return `<div class="${cls}" id="${it.id}">
    <div class="meta"><span>${it.published}</span>${badges}<span>${lines}</span></div>
    <h3><a href="${it.url}" target="_blank">${it.title_zh || it.title}</a></h3>
    <div class="orig">${it.title}</div>
    <div class="oneliner">${it.one_liner}</div>
    <div class="actions">${links}
      ${it.claims.length ? `<span class="toggle" data-n="${it.claims.length}" onclick="toggleDetail(this)">展开论断（${it.claims.length}）▼</span>` : ""}
    </div>
    <div class="detail">${claims ? claims : ""}
      ${ents ? `<div class="ents"><span class="lbl">相关:</span>${ents}</div>` : ""}
    </div>
  </div>`;
}

function render() {
  let list = DATA.items.filter(match);
  if (state.sort === "top") {
    list = [...list].sort((a, b) =>
      (REL_RANK[a.relevance] - REL_RANK[b.relevance]) || (a.published < b.published ? 1 : -1));
  }
  document.getElementById("list").innerHTML = list.map(card).join("");
  document.getElementById("empty").style.display = list.length ? "none" : "block";
  document.getElementById("foot").innerHTML =
    `显示 ${list.length}/${DATA.stats.papers + DATA.stats.releases} 条 · 数据与引擎：<a href="${DATA.repo_url}" target="_blank">LLM-Reading</a>` +
    (state.ent ? ` · 实体过滤 <b onclick="filterEnt('${state.ent}')" style="cursor:pointer">${ENT[state.ent] || state.ent} ✕</b>` : "");
}
renderLines();
render();
</script>
</body>
</html>
"""


def main() -> int:
    data = build_data()
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = TEMPLATE.replace("__DATA__", payload)
    SITE.mkdir(exist_ok=True)
    out = SITE / "index.html"
    out.write_text(html, encoding="utf-8")
    print(f"→ {out}（论文 {data['stats']['papers']} + 版本 {data['stats']['releases']}, "
          f"{len(html) // 1024} KB）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
