# LLM-Reading —— 音视频领域信息整合引擎

目标不是再做一条「抓取→总结→推送」的管道，而是建一个**垂类技术领域的信息整合引擎**：
多来源信息归一化沉淀为可积累的知识基底（kb），推送分发、垂类专家问答、训练语料
都只是基底之上的读取端。

## 形状

```
信息来源（可插拔 adapter）               基底（核心资产）              消费端（可插拔 reader）
─────────────────────────          ──────────────────────     ─────────────────────────
arXiv / 顶会          ─┐                                      ┌─→ 周报 digest（时间性读取）
JVET/MPEG/AOM 文档     ├→ 归一化 → 实体对齐 → 落地沉淀 → 关联 ─→ ├─→ 垂类专家 RAG（结构性读取）
开源 codec 仓库/release│   item     实体注册表   kb/      graph  ├─→ SFT/预训练语料（批量导出）
公司技术博客/行业媒体   │                                      └─→ 趋势分析 / 技术雷达
基准 / 专利池 / 芯片   ─┘
```

与「信息流分发」的本质区别：中间有一层**统一数据模型 + 实体注册表**，
信息流过即沉淀、互相关联、持续复利——而不是消费一次即焚。

## 目录

| 路径 | 内容 |
|---|---|
| [kb/](kb/README.md) | **知识基底**：schema、实体注册表（90 实体）、结构化信息项 |
| [docs/](docs/README.md) | 长文精读笔记（2026-06 六篇视频/图像压缩论文）+ 谱系索引 |
| `paper/` | 论文 PDF 留档（arXiv ID 命名） |
| `scripts/` | 工具脚本（当前：基底校验） |

`kb/items/*` 的 `summaries.deep_dive` 指回 `docs/` 长文：推送读一句话、问答读论断、深读跳笔记。

## 当前状态

- ✅ 学术源（arXiv）全链路闭环：`fetch_arxiv`（拉取/实体对齐/队列）→ `llm_review`（glm-5.3-flash 精度终审 + 中文初筛）→ `kb/items/`（过校验落库）
- ✅ 基底：**35 个信息项**（6 篇手工精读回填 + 29 篇 pipeline 自动审阅）、135 条论断、111 处量化指标、90 实体
- ✅ 首轮 150 天回补：队列 56 条（reviewed 29 / 规则 skipped 26 / LLM skipped 1）
- ✅ 消费端 v0：`make_digest` 按时间窗+研究主线生成周报 → `docs/digests/`
- 🔶 deep_read 深读（试点中）：`deep_read` 下载 PDF → glm-5.3 流式全文精读 → `docs/auto/` 笔记回链 item
- ⬜ 第二信息源：JVET 文档列表（站点对数据中心 IP 不开放，可能需要成员凭据或改用 AOMedia GitHub 等开放源）
- ⬜ 消费端：RAG 问答 → 语料导出（按 source.license 过滤）

## 设计决策（为什么长这样）

1. **先定 schema 再接管道**：所有 adapter/reader 都以 kb/ 契约为接口，避免每条管道自成孤岛。
2. **实体闭集是精度来源**：检索过滤 = 新信息与注册表实体的匹配，而非全文相似度；
   这是垂类引擎相对通用引擎的可胜之处。
3. **翻译在入库时完成**（`title_zh`/`summaries.*_zh`），消费端不再各翻一遍。
4. **训练语料是副产品不是目标**：基底做好后导出只是多写一个 reader；
   版权约束（专利/JVET 文档 ≠ arXiv）在 `source.license` 字段里随行。

## 工具

```bash
uv run --with pyyaml python scripts/validate_kb.py                        # 校验基底一致性
uv run --with pyyaml python scripts/fetch_arxiv.py                        # 增量拉取（默认回看 30 天）
uv run --with pyyaml python scripts/fetch_arxiv.py --days 150             # 补历史窗口
```
