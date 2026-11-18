"""Build private, browser-local rate and decoding time worksheets from sourced claims."""
import json
from pathlib import Path
import re
from urllib.parse import quote

from site_details import detail_url


def write_sheets(items: list[dict], site: Path) -> dict:
    template = Path(__file__).with_name("retest.html").read_text(encoding="utf-8")
    links = {}
    slugs = set()
    for item in items:
        protocol = item.get("retest")
        if not protocol:
            continue
        slug = protocol["slug"]
        if not re.fullmatch(r"[a-z0-9-]+", slug) or slug in slugs:
            raise ValueError(f"Invalid or duplicate worksheet slug: {slug}")
        slugs.add(slug)
        claims = {c["id"]: c for c in item["claims"] if "id" in c}
        cases = {}
        filename = f"retest-{slug}.html"
        links[item["id"]] = {}
        for key, label in protocol["configurations"].items():
            claim = claims[key]
            metrics = {m["name"]: m["value"] for m in claim["metrics"] if "name" in m}
            time_metric = "解码时间降低" if "解码时间降低" in metrics else "解码时间增加"
            sign = -1 if time_metric == "解码时间降低" else 1
            cases[key] = {
                "label": label, "claim": detail_url(item["id"]) + "/" + quote(key),
                "source": claim["evidence_url"], "sourceLabel": claim["evidence"],
                "rate": -float(metrics["码率节省"].removesuffix("%")),
                "time": sign * float(metrics[time_metric].removesuffix("%")),
            }
            links[item["id"]][key] = f"{filename}#{quote(key)}"
        data = {**protocol, "configurations": cases, "item": item["id"]}
        payload = json.dumps(data, ensure_ascii=False).replace("<", r"\u003c")
        (site / filename).write_text(template.replace("__PROTOCOL__", payload), encoding="utf-8")
    return links
