#!/usr/bin/env python3
"""站点生成器（消费端 v1）：基底 → 自包含单页前端 site/index.html。

设计约束：
- 零依赖、单文件：数据以 JSON 内联，file:// 直开或托管到 GitHub Pages 均可
- 只读 kb/（基底是唯一事实源），深读笔记链接指向 GitHub 仓库对应文件
- 重新生成即更新：uv run --with pyyaml python scripts/make_site.py
"""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ITEMS = ROOT / "kb" / "items" / "papers"
SITE = ROOT / "site"
REPO_URL = "https://github.com/bitchenhui/LLM-Reading"

LINE_NAMES = {
    "traditional_codec_opt": "传统编码器优化",
    "learned_codec": "学习式编码",
    "coding_for_machines": "面向机器的编码",
    "generative_compression": "生成式压缩",
    "inr_representation": "INR 表示压缩",
    "systems_deployment": "系统与部署",
}


def load(p: Path):
    return yaml.safe_load(open(p, encoding="utf-8"))


def metric_text(m: dict) -> str:
    label = m.get("name") or m.get("ref", "").split(":")[-1]
    val = m.get("value", "")
    unit = m.get("unit", "")
    scope = m.get("scope", "")
    if isinstance(val, (int, float)):
        val = f"{val}{unit}" if unit else str(val)
    return f"{label} {val}" + (f"（{scope}）" if scope else "")


def build_data() -> dict:
    items = []
    for p in sorted(ITEMS.glob("*.yaml")):
        d = load(p)
        deep = d["summaries"].get("deep_dive")
        items.append({
            "id": d["id"],
            "title": d["title"],
            "title_zh": d.get("title_zh"),
            "published": d["time"]["published"],
            "collected": d["time"]["collected"],
            "url": d["source"]["url"],
            "lines": d.get("research_lines") or [],
            "relevance": d["assessment"]["relevance"],
            "decision": d["assessment"]["decision"],
            "one_liner": d["summaries"].get("one_liner_zh", ""),
            "abstract": d["summaries"].get("abstract_zh"),
            "claims": [
                {"statement": c["statement"],
                 "metrics": [metric_text(m) for m in c.get("metrics", [])],
                 "confidence": c.get("confidence", "reported"),
                 "evidence": c.get("evidence", "")}
                for c in d.get("claims", [])
            ],
            "entities": [e["ref"] for e in d.get("entities", [])],
            "tags": d["summaries"].get("tags", []),
            "deep_dive_url": f"{REPO_URL}/blob/main/{deep}" if deep else None,
            "manual": d.get("provenance", {}).get("actor") == "manual-backfill",
        })
    items.sort(key=lambda x: (x["published"], x["relevance"]), reverse=True)
    n_claims = sum(len(i["claims"]) for i in items)
    return {
        "generated": date.today().isoformat(),
        "repo_url": REPO_URL,
        "line_names": LINE_NAMES,
        "stats": {
            "items": len(items),
            "claims": n_claims,
            "deep_reads": sum(1 for i in items if i["deep_dive_url"]),
        },
        "items": items,
    }


TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>音视频编码信息引擎</title>
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
.wrap { max-width: 1080px; margin: 0 auto; padding: 32px 20px 80px; }
header h1 { font-size: 22px; letter-spacing: .5px; }
header .sub { color: var(--dim); font-size: 13px; margin-top: 4px; }
.stats { display: flex; gap: 12px; margin: 18px 0 22px; flex-wrap: wrap; }
.stat { background: var(--panel); border: 1px solid var(--border); border-radius: 10px;
  padding: 10px 16px; font-size: 13px; color: var(--dim); }
.stat b { color: var(--text); font-size: 18px; margin-right: 4px; }
.filters { position: sticky; top: 0; background: var(--bg); padding: 12px 0;
  border-bottom: 1px solid var(--border); z-index: 5; }
.chips { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 10px; }
.chip { border: 1px solid var(--border); background: var(--panel); color: var(--dim);
  border-radius: 999px; padding: 3px 12px; font-size: 12.5px; cursor: pointer; user-select: none; }
.chip.on { background: var(--accent); border-color: var(--accent); color: #fff; }
.row { display: flex; gap: 10px; flex-wrap: wrap; }
input[type=search], select { background: var(--panel); border: 1px solid var(--border);
  color: var(--text); border-radius: 8px; padding: 6px 10px; font-size: 13px; }
input[type=search] { flex: 1; min-width: 200px; }
.card { background: var(--card); border: 1px solid var(--border); border-radius: 12px;
  padding: 16px 18px; margin-bottom: 14px; }
.card.manual { border-left: 3px solid var(--green); }
.card.top { border-left: 3px solid var(--accent); }
.meta { display: flex; gap: 8px; align-items: center; flex-wrap: wrap;
  font-size: 12px; color: var(--dim); margin-bottom: 6px; }
.badge { padding: 1px 8px; border-radius: 6px; font-size: 11.5px; font-weight: 600; }
.b-high { background: rgba(91,157,255,.18); color: var(--accent); }
.b-medium { background: rgba(245,166,35,.15); color: var(--orange); }
.b-low { background: rgba(229,83,75,.15); color: var(--red); }
.b-deep { background: rgba(76,195,138,.15); color: var(--green); }
.b-sum { background: rgba(177,140,255,.15); color: var(--purple); }
h3 { font-size: 15.5px; font-weight: 600; }
h3 a { color: var(--text); text-decoration: none; }
h3 a:hover { color: var(--accent); }
.orig { color: var(--dim); font-size: 12.5px; margin-top: 1px; }
.oneliner { font-size: 13.5px; margin: 8px 0 4px; color: #c6cdbe; }
.ents { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 8px; }
.ent { font-size: 11.5px; color: var(--dim); background: var(--panel);
  border: 1px solid var(--border); border-radius: 5px; padding: 1px 7px; cursor: pointer; }
.ent:hover { color: var(--accent); border-color: var(--accent); }
.claims-toggle { margin-top: 10px; font-size: 12.5px; color: var(--accent);
  cursor: pointer; user-select: none; }
.claims { display: none; margin-top: 8px; border-top: 1px dashed var(--border); padding-top: 8px; }
.claim { font-size: 13px; margin-bottom: 8px; }
.claim .m { color: var(--green); font-size: 12.5px; margin-left: 6px; }
.claim .ev { color: var(--dim); font-size: 11.5px; }
.links { margin-top: 10px; display: flex; gap: 14px; font-size: 12.5px; }
.links a { color: var(--accent); text-decoration: none; }
.empty { color: var(--dim); text-align: center; padding: 60px 0; }
footer { color: var(--dim); font-size: 12px; margin-top: 30px; text-align: center; }
footer a { color: var(--dim); }
</style>
</head>
<body>
<div class="wrap">
<header>
  <h1>音视频编码 · 信息引擎</h1>
  <div class="sub">视频/图像压缩领域 — 论文检索 · 精读 · 结构化知识基底</div>
</header>
<div class="stats" id="stats"></div>
<div class="filters">
  <div class="chips" id="lineChips"></div>
  <div class="row">
    <input type="search" id="q" placeholder="搜索标题 / 摘要 / 论断 / 实体…">
    <select id="rel"><option value="">全部相关性</option><option value="high">高相关</option><option value="medium">中相关</option><option value="low">低相关</option></select>
    <select id="dec"><option value="">全部处置</option><option value="deep_read">深读</option><option value="summary_only">仅摘要</option></select>
  </div>
</div>
<div id="list"></div>
<div class="empty" id="empty" style="display:none">无匹配条目</div>
<footer id="foot"></footer>
</div>
<script>
const DATA = __DATA__;
const LINE = DATA.line_names;
const REL_ZH = { high: "高相关", medium: "中相关", low: "低相关" };
const DEC_ZH = { deep_read: "深读", summary_only: "仅摘要" };
const state = { lines: new Set(), q: "", rel: "", dec: "", ent: "" };

document.getElementById("stats").innerHTML =
  `<div class="stat"><b>${DATA.stats.items}</b>信息项</div>` +
  `<div class="stat"><b>${DATA.stats.claims}</b>结构化论断</div>` +
  `<div class="stat"><b>${DATA.stats.deep_reads}</b>深读笔记</div>` +
  `<div class="stat">更新 ${DATA.generated}</div>`;

const chips = document.getElementById("lineChips");
Object.entries(LINE).forEach(([k, name]) => {
  const n = DATA.items.filter(i => i.lines.includes(k)).length;
  const el = document.createElement("span");
  el.className = "chip"; el.textContent = `${name} ${n}`; el.dataset.k = k;
  el.onclick = () => { state.lines.has(k) ? state.lines.delete(k) : state.lines.add(k);
    el.classList.toggle("on"); render(); };
  chips.appendChild(el);
});
const allChip = document.createElement("span");
allChip.className = "chip on"; allChip.textContent = "全部";
allChip.onclick = () => { state.lines.clear();
  document.querySelectorAll("#lineChips .chip[data-k]").forEach(c => c.classList.remove("on"));
  render(); };
chips.prepend(allChip);

document.getElementById("q").oninput = e => { state.q = e.target.value.toLowerCase(); render(); };
document.getElementById("rel").onchange = e => { state.rel = e.target.value; render(); };
document.getElementById("dec").onchange = e => { state.dec = e.target.value; render(); };
window.filterEnt = ref => { state.ent = state.ent === ref ? "" : ref; render(); };

function match(it) {
  if (state.lines.size && !it.lines.some(l => state.lines.has(l))) return false;
  if (state.rel && it.relevance !== state.rel) return false;
  if (state.dec && it.decision !== state.dec) return false;
  if (state.ent && !it.entities.includes(state.ent)) return false;
  if (state.q) {
    const hay = (it.title + " " + (it.title_zh || "") + " " + it.one_liner + " " +
      (it.abstract || "") + " " + it.entities.join(" ") + " " +
      it.claims.map(c => c.statement).join(" ")).toLowerCase();
    if (!hay.includes(state.q)) return false;
  }
  return true;
}

function card(it) {
  const ents = it.entities.slice(0, 12).map(e =>
    `<span class="ent" onclick="filterEnt('${e}')">${e}</span>`).join("");
  const claims = it.claims.map(c => {
    const m = c.metrics.map(x => `<span class="m">▸ ${x}</span>`).join(" ");
    const ev = c.evidence ? ` <span class="ev">[${c.evidence}]</span>` : "";
    return `<div class="claim">· ${c.statement}${m}${ev}</div>`;
  }).join("");
  const links = [`<a href="${it.url}" target="_blank">arXiv ↗</a>`]
    .concat(it.deep_dive_url ? [`<a href="${it.deep_dive_url}" target="_blank">深读笔记 ↗</a>`] : [])
    .join("");
  const cls = it.manual ? "card manual" : (it.relevance === "high" ? "card top" : "card");
  const lines = it.lines.map(l => LINE[l] || l).join(" / ") || "未分类";
  return `<div class="${cls}" id="${it.id}">
    <div class="meta"><span>${it.published}</span>
      <span class="badge b-${it.relevance}">${REL_ZH[it.relevance] || it.relevance}</span>
      <span class="badge ${it.decision === "deep_read" ? "b-deep" : "b-sum"}">${DEC_ZH[it.decision] || it.decision}</span>
      <span>${lines}</span></div>
    <h3><a href="${it.url}" target="_blank">${it.title_zh || it.title}</a></h3>
    <div class="orig">${it.title}</div>
    <div class="oneliner">${it.one_liner}</div>
    ${it.claims.length ? `<div class="claims-toggle" onclick="const el=this.nextElementSibling;el.style.display=el.style.display==='block'?'none':'block';this.textContent=el.style.display==='block'?'▲ 收起论断':'▼ 展开论断（'+${it.claims.length}）'">▼ 展开论断（${it.claims.length}）</div><div class="claims">${claims}</div>` : ""}
    <div class="ents">${ents}</div>
    <div class="links">${links}</div>
  </div>`;
}

function render() {
  const list = DATA.items.filter(match);
  document.getElementById("list").innerHTML = list.map(card).join("");
  document.getElementById("empty").style.display = list.length ? "none" : "block";
  document.getElementById("foot").innerHTML =
    `共 ${list.length}/${DATA.stats.items} 条 · 数据源：<a href="${DATA.repo_url}" target="_blank">LLM-Reading kb/</a>` +
    (state.ent ? ` · 实体过滤: <b onclick="filterEnt('${state.ent}')" style="cursor:pointer">${state.ent} ✕</b>` : "");
}
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
    print(f"→ {out}（{data['stats']['items']} items, {data['stats']['claims']} claims, "
          f"{len(html) // 1024} KB）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
