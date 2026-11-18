"""Generate static, addressable item and claim views in small HTML bundles."""
from collections import defaultdict
from hashlib import sha256
from html import escape
from pathlib import Path
from urllib.parse import quote, urlsplit


def claim_id(claim: dict) -> str:
    return claim.get("id") or sha256(claim["statement"].encode()).hexdigest()[:12]


def detail_url(item_id: str) -> str:
    bucket = sha256(item_id.encode()).hexdigest()[0]
    return f"details/{bucket}.html#{quote(item_id, safe=':')}"


def link(url: str, label: str) -> str:
    if urlsplit(url).scheme not in {"http", "https"}:
        return escape(label)
    return f'<a href="{escape(url, quote=True)}">{escape(label)}</a>'


def claim_html(item: dict, claim: dict, repo_url: str) -> str:
    statement = claim["statement"]
    key = claim_id(claim)
    anchor = escape(f"{item['id']}/{key}", quote=True)
    lines = []
    for metric in claim.get("metrics", []):
        name = metric.get("name") or metric.get("ref", "").removeprefix("metric:")
        value = str(metric["value"])
        unit = str(metric.get("unit") or "")
        if unit and not value.endswith(unit):
            value += unit
        lines.append(f'<li><strong>{escape(name)} {escape(value)}</strong>　'
                     f'{escape(str(metric.get("scope") or "口径待补"))}</li>')
    evidence = claim.get("evidence", "")
    source = link(claim["evidence_url"], evidence) if claim.get("evidence_url") else escape(evidence)
    note = item["summaries"].get("deep_dive")
    section = claim.get("note_section")
    if note and section:
        source += " · " + link(f"{repo_url}/blob/main/{quote(note)}#{quote(section)}", "精读对应章节")
    confidence = {"inferred": "推断", "reported": "来源报告", "verified": "已复测"}.get(claim.get("confidence"))
    return (f'<section id="{anchor}"><p>{escape(statement)}</p><ul>{"".join(lines)}</ul>'
            f'<small>{escape(confidence or "")} {source}</small> '
            f'<a class="permalink" href="#{anchor}">论断链接</a></section>')


def write_details(items: list[dict], site: Path, repo_url: str) -> None:
    bundles = defaultdict(list)
    for item in items:
        iid = item["id"]
        summary = item["summaries"]
        title = item.get("title_zh") or item["title"]
        links = [link(item["source"]["url"], "原文")]
        if summary.get("deep_dive"):
            links.append(link(f'{repo_url}/blob/main/{quote(summary["deep_dive"])}', "精读笔记"))
        claims = "".join(claim_html(item, claim, repo_url) for claim in item["claims"])
        body = (f'<article id="{escape(iid)}"><small>{escape(item["time"]["published"])} · '
                f'{escape(item["source"]["channel"])}</small><h1>{escape(title)}</h1>'
                f'<p>{escape(summary.get("abstract_zh") or summary["one_liner_zh"])}</p>'
                f'<nav>{" · ".join(links)}</nav><h2>论断与证据</h2>{claims}</article>')
        filename = detail_url(iid).split("#")[0]
        bundles[filename].append(body)

    (site / "details").mkdir(parents=True, exist_ok=True)
    for filename, articles in bundles.items():
        (site / filename).write_text(PAGE.replace("<!--items-->", "".join(articles)), encoding="utf-8")


PAGE = """<!doctype html><html lang="zh-CN"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>条目详情 · 音视频信息引擎</title>
<style>
:root{color-scheme:dark}body{margin:0;background:#0f1115;color:#e4e7ee;font:16px/1.75 system-ui,sans-serif}
main{max-width:760px;margin:auto;padding:24px 20px 72px;overflow-wrap:anywhere}
article{display:none}article:target,article:has(section:target){display:block}
h1{font-size:clamp(21px,4vw,29px);line-height:1.35}h2{font-size:19px;margin-top:30px}
a{color:#81b4ff}small,.permalink{color:#aab5c8;font-size:13px}section{padding:14px 0;border-top:1px solid #343c4b}
section:target{border-color:#81b4ff}ul{padding-left:22px}nav{margin:16px 0}section p{margin:0 0 6px}
</style><main><nav><a href="../index.html">首页与站内搜索</a></nav><!--items--></main>
<script>
const current = document.getElementById(decodeURIComponent(location.hash.slice(1)));
if (current) document.title = current.closest('article').querySelector('h1').textContent + ' · 音视频信息引擎';
</script></html>"""
