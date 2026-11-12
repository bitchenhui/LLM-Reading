# LLM-Reading —— 音视频领域信息整合引擎

不做「抓取→总结→推送」的一次性管道，而是一个**垂类技术领域的信息整合引擎**：
多来源信息归一化沉淀为可积累的知识基底（`kb/`），分发、问答、训练语料都只是基底之上的读取端。

**在线前端：<https://bitchenhui.github.io/LLM-Reading/>**（push 到 main 自动从基底重建）

## 架构与完成度

```
信息来源（adapter）                     基底（kb/）                  消费端（reader）
─────────────────────────          ─────────────────────      ─────────────────────────
arXiv 论文          ✅ 闭环     ─┐                            ┌─→ 网页前端 + Pages      ✅
codec 仓库 releases 🔶 放量中   ─┼→ 归一化 → 实体对齐 → 落库 ─→ ├─→ digest 周报          ✅
JVET 标准提案       ⏸ 无凭据    ─┤   item    实体注册表(90)    ├─→ RAG 垂类问答         ⬜
av2-spec tags       ⬜ 下一源    ─┘   队列    LLM 审阅/深读     └─→ SFT/预训练语料导出   ⬜
```

| 层 | 状态 | 说明 |
|---|---|---|
| 知识基底 | ✅ | item/entity schema、90 实体注册表、一致性校验（引用完整性/词表/口径） |
| arXiv 学术源 | ✅ | `fetch_arxiv` 拉取→实体对齐打分→队列；`llm_review`(glm-5.3-flash) 精度终审+中文初筛；首轮 150 天回补 56 条 |
| 深读管线 | 🔶 | `deep_read`(glm-5.3 流式) 下载 PDF→全文精读→`docs/auto/` 笔记回链 item；29 篇候选分批放量中 |
| 仓库 release 源 | 🔶 | `fetch_releases` 监控 VVenC/VVdec/SVT-AV1/libavif/dav1d/kvazaar；51 条入队，LLM 审阅中（工业落地信号） |
| 网页前端 | ✅ | 自包含单页：时间线/6 主线筛选(带计数)/全文检索/论断展开(带口径)/实体过滤/深读回链 |
| digest 周报 | ✅ | `make_digest` 按时间窗+主线分组 → `docs/digests/` |
| JVET 源 | ⏸ | 站点需成员凭据（暂缓）；AV2 标准文本在 `AOMediaCodec/av2-spec` 公开，tags 跟踪为下一增量 |
| RAG / 语料导出 | ⬜ | 蓝图后半段；语料导出按 `source.license` 分级过滤 |

## 目录

| 路径 | 内容 |
|---|---|
| [kb/](kb/README.md) | **基底**：schema、实体注册表、结构化信息项（入库契约与词表见其 README） |
| `kb/items/papers/` `kb/items/releases/` | 信息项（按 type 分目录；`docs/` 长文与 `deep_dive` 字段互链） |
| `queue/` | 候选队列（pending/skipped/reviewed；文件存在即「已见」，天然幂等去重） |
| [docs/](docs/README.md) | 手工精读笔记（2026-06 六篇）+ `docs/auto/` 自动深读 + `docs/digests/` 周报 |
| `paper/` | 论文 PDF 留档（arXiv ID 命名） |
| `scripts/` | 引擎全部代码（见下） |
| `config/` | 各源口径配置 + `llm.local.yaml`（gitignore，含密钥） |
| `site/` | 网页前端（生成物，勿手编） |

## 使用

```bash
# 检索：arXiv 增量 + 仓库 releases
uv run --with pyyaml python scripts/fetch_arxiv.py [--days N] [--max-results N]
uv run --with pyyaml python scripts/fetch_releases.py

# 审阅：精度终审 + 中文初筛 → 落库（--limit 先试跑；--dry-run 不落库）
uv run --with pyyaml python scripts/llm_review.py

# 深读：glm-5.3 全文精读 deep_read 候选 → docs/auto/
uv run --with pyyaml --with pymupdf python scripts/deep_read.py --limit 3

# 消费：周报 + 网页
uv run --with pyyaml python scripts/make_digest.py --days 7
uv run --with pyyaml python scripts/make_site.py

# 一致性校验（任何入库后都应跑）
uv run --with pyyaml python scripts/validate_kb.py
```

LLM 配置：`config/llm.local.yaml`（zhipu GLM，OpenAI Responses 协议，SSE 流式；
密钥不入库）。修改基底结构前先读 [kb/README.md](kb/README.md) 的契约与词表。

## 设计决策

1. **先定 schema 再接管道**：adapter/reader 都以 `kb/` 契约为接口，避免管道孤岛。
2. **实体闭集是精度来源**：检索过滤 = 新信息与注册表实体（90 个，人工可维护）的匹配，
   而非全文相似度；这是垂类引擎相对通用引擎的可胜之处。
3. **claims 是引擎与摘要的分水岭**：每条论断带量化指标与口径（scope），无口径不入库；
   `confidence` 区分 reported/verified/inferred。
4. **翻译入库时完成**（title_zh/summaries），消费端不再翻译。
5. **训练语料是副产品不是目标**：基底建成后导出只是多一个 reader；版权约束在
   `source.license` 随行（专利/JVET 文档 ≠ arXiv）。

## 数据快照（2026-11-12）

基底 35 论文 items（135 论断/111 量化指标）+ 深读笔记 10 篇 + release items 放量中；
队列：arXiv 56 条全处置，releases 51 条审阅中。

## Roadmap

- 近期：深读放量收尾（29 篇）；`av2-spec` tags 源；`fetch→review→digest→site` 定时化（cron/Actions）
- 中期：RAG 垂类问答（kb claims + 深读笔记为语料）；digest 接 IM 推送；增量去重的跨源实体对齐强化
- 远期：语料导出（license 分级）→ 垂类微调；趋势分析/技术雷达 reader
