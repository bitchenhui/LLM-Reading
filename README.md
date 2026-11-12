# LLM-Reading —— 音视频领域信息整合引擎

不做「抓取→总结→推送」的一次性管道，而是一个**垂类技术领域的信息整合引擎**：
多来源信息归一化沉淀为可积累的知识基底（`kb/`），分发、问答、训练语料都只是基底之上的读取端。

**在线前端：<https://bitchenhui.github.io/LLM-Reading/>**（push 到 main 自动从基底重建）

## 架构与完成度（v1 已交付）

```
信息来源（adapter）                       基底（kb/）                    消费端（reader）
─────────────────────────            ───────────────────────      ─────────────────────────
arXiv 论文（八类 track） ✅       ─┐                              ┌─→ 网页前端 + Pages      ✅
codec 仓库 releases      ✅       ─┼→ 归一化 → 实体对齐 → 队列 ─→ ├─→ digest 周报          ✅
IAMF/音频标准 releases   ✅       ─┤   item    实体注册表(116)     ├─→ RAG 问答（ask）      ✅
JVET/MPEG 标准提案       ⏸ 无凭据 ─┘   幂等去重  LLM 审阅/深读     └─→ SFT 语料导出        ✅

⏰ 每日 09:30（北京）GitHub Actions 无人值守：拉取→审阅→深读×3→周报→语料→校验→提交推送 ✅（已实测）
```

| 层 | 状态 | 说明 |
|---|---|---|
| 领域分类 | ✅ | **八类 taxonomy**：视频/图像编码（核心）、音频编码、流媒体传输、质量评估、处理增强、沉浸式/三维、标准生态、自我改进 AI（RSI/EoH） |
| 知识基底 | ✅ | item/entity schema（domain+research_line 两层）、116 实体、一致性校验 |
| arXiv 学术源 | ✅ | 八 track 检索→实体对齐打分→队列→`llm_review`(glm-5.3-flash) domain 感知终审（非核心域自动 summary 降级）；全年回补完成 |
| 深读管线 | ✅ | `deep_read`(glm-5.3 流式) 全文精读→`docs/auto/` 笔记回链；**候选清零** |
| 仓库 release 源 | ✅ | VVenC/VVdec/SVT-AV1/libavif/dav1d/kvazaar/IAMF 的 GitHub releases |
| JVET 源 | ⏸ | 需成员凭据；AV2 spec 仓库为静态快照（无版本信号）——标准线是 v1 的已知空白 |
| 网页前端 | ✅ | 时间线/八类筛选/主线筛选/全文检索/论断展开/实体过滤/深读回链，Pages 自动部署 |
| digest / RAG / 语料 | ✅ | `make_digest` 周报；`ask.py` 实体优先问答（引用溯源+基底未覆盖显式声明）；`export_corpus.py` SFT 问答对+长文（license 边界内） |

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

## 数据快照（2026-11-12，v1 交付）

- **186 个信息项**：视频/图像编码 125（核心域）· 自我改进 AI 46 · 音频编码 9 · 沉浸式 3 · 质量评估 2 · 处理增强 1 · 流媒体/标准生态 0（实体覆盖尚薄，随 daily 增长）
- **743 条结构化论断 / 399 处带口径的量化指标 / 116 个实体**
- **69 篇深读笔记**（63 篇自动 + 6 篇手工），deep_read 候选全部消化
- 队列 372 条全处置（幂等去重）；SFT 语料 37+ 问答对、35+ 长文（随 daily 刷新）
- 每日 09:30（北京）Actions 自动运行，前端/周报/语料随动

## Roadmap（v2 候选）

- 标准线接入：JVET/MPEG 成员凭据，或 AOMedia 工作组公开信号的更深挖掘
- 检索升级：embedding 召回补充实体匹配；跨源实体对齐（同名工作 arXiv↔blog↔repo）
- digest 接 IM 推送（飞书/钉钉/Slack webhook）
- 趋势分析 reader：按实体/主线的时间序列信号（谁在升温）
- 垂类微调：语料攒到千级后启动 SFT 实验
