#!/usr/bin/env python3
"""本地服务：托管前端 + /api/ask 知识库问答代理。

前端（site/index.html）部署在 GitHub Pages 上时"本周新成果/知识库"可读，
问答需要密钥——为不在公开页面暴露 zhipu key，问答走本地服务：

    uv run --with pyyaml python scripts/serve.py     # http://127.0.0.1:8931

前端自动探测同源 /api/ask；Pages 上访问时提示改用本地服务。
"""
from __future__ import annotations

import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import yaml  # noqa: E402

from ask import answer_question  # noqa: E402

SITE = ROOT / "site"
PORT = 8931


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):  # 安静些
        print(f"[{self.command}] {self.path}", file=sys.stderr)

    def _send(self, code: int, body: bytes, ctype: str):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self._send(204, b"", "text/plain")

    def do_GET(self):
        path = self.path.split("?")[0]
        if path in ("/", "/index.html"):
            self._send(200, (SITE / "index.html").read_bytes(), "text/html; charset=utf-8")
        else:
            self._send(404, b"not found", "text/plain")

    def do_POST(self):
        if self.path != "/api/ask":
            self._send(404, b"not found", "text/plain")
            return
        try:
            length = int(self.headers.get("Content-Length", 0))
            req = json.loads(self.rfile.read(length) or b"{}")
            question = str(req.get("question", "")).strip()
            if not question:
                self._send(400, json.dumps({"error": "question required"}).encode(),
                           "application/json")
                return
            print(f"[ask] {question[:80]}", file=sys.stderr, flush=True)
            r = answer_question(question)
            self._send(200, json.dumps(r, ensure_ascii=False).encode(), "application/json")
        except Exception as e:  # noqa: BLE001
            self._send(500, json.dumps({"error": str(e)}, ensure_ascii=False).encode(),
                       "application/json")


def main() -> int:
    addr = ("127.0.0.1", PORT)
    print(f"音视频信息引擎 · 本地服务 http://127.0.0.1:{PORT}"
          f"（问答可用；静态页与 Pages 版一致）")
    ThreadingHTTPServer(addr, Handler).serve_forever()
    return 0


if __name__ == "__main__":
    sys.exit(main())
