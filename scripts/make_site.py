#!/usr/bin/env python3
"""站点生成器 v3：两页式前端（用户定义的形态）。

- 页签一「本周新成果」：最近 7 天新条目，按八大类分组
- 页签二「知识库」：领域问答（本地 serve.py 提供 /api/ask）+ 八大类领域综述
  （kb/synthesis/*.md，glm-5.3 基于全量条目合成的"发展历程/技术主线/关键问题"）

零依赖单文件；重新生成：uv run --with pyyaml python scripts/make_site.py
"""
from __future__ import annotations

import json
import sys
from datetime import date, timedelta
from pathlib import Path

import yaml

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
    return yaml.safe_load(open(p, encoding="utf-8"))


def build_data() -> dict:
    cutoff = (date.today() - timedelta(days=WEEK_DAYS)).isoformat()
    all_items = []
    for p in sorted(ITEMS.glob("*/*.yaml")):
        d = load(p)
        deep = d["summaries"].get("deep_dive")
        all_items.append({
            "id": d["id"],
            "type": d["type"],
            "domain": d.get("domain") or CORE,
            "title": d.get("title_zh") or d["title"],
            "orig_title": d["title"] if d.get("title_zh") else "",
            "published": d["time"]["published"],
            "url": d["source"]["url"],
            "one_liner": d["summaries"].get("one_liner_zh", ""),
            "deep": f"{REPO_URL}/blob/main/{deep}" if deep else None,
        })

    week = [i for i in all_items if i["published"] >= cutoff]
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

    return {
        "generated": date.today().isoformat(),
        "cutoff": cutoff,
        "repo_url": REPO_URL,
        "domain_names": DOMAIN_NAMES,
        "domain_order": DOMAIN_ORDER,
        "core": CORE,
        "stats": {
            "total": len(all_items),
            "week": len(week),
            "domains": {k: sum(1 for i in all_items if i["domain"] == k)
                        for k in DOMAIN_ORDER},
        },
        "week_by_domain": {k: by_domain.get(k, []) for k in
                           [CORE] + [d for d in DOMAIN_ORDER if d != CORE]},
        "items_by_domain": {k: items_by_domain.get(k, []) for k in
                            [CORE] + [d for d in DOMAIN_ORDER if d != CORE]},
        "synthesis": synthesis,
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
<div class="tabs">
  <div class="tab on" id="tab-week" onclick="showTab('week')">本周新成果</div>
  <div class="tab" id="tab-kb" onclick="showTab('kb')">知识库 · 问答</div>
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
</div>

<footer id="foot"></footer>
</div>
<script>
const DATA = __DATA__;
const DN = DATA.domain_names;

document.getElementById("weekNote").innerHTML =
  `最近 7 天（自 ${DATA.cutoff}）新增 <b>${DATA.stats.week}</b> 条 · 基底累计 ${DATA.stats.total} 条 · 更新 ${DATA.generated}`;

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
    <h3><a href="${it.url}" target="_blank">${it.title}</a></h3>
    <div class="oneliner">${it.one_liner}</div>
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
wl.innerHTML = html || `<div class="empty">最近 7 天无新增（引擎每日 09:30 自动拉取）</div>`;

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
  const links = [`<a href="${it.url}" target="_blank">${it.title}</a>`]
    .concat(it.deep ? [`<a href="${it.deep}" target="_blank" style="font-weight:400;font-size:12px;color:var(--accent);">精读笔记↗</a>`] : []).join(" ");
  return `<div class="row-item"${visible ? "" : ' style="display:none"'}>
    <div class="l1"><span class="d">${it.published}</span>${badge(it)}${links}</div>
    <div class="ol">${it.one_liner}</div>
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

function showTab(t) {
  document.getElementById("view-week").style.display = t === "week" ? "" : "none";
  document.getElementById("view-kb").style.display = t === "kb" ? "" : "none";
  document.getElementById("tab-week").classList.toggle("on", t === "week");
  document.getElementById("tab-kb").classList.toggle("on", t === "kb");
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
    data = build_data()
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
