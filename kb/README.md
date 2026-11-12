# kb/ —— 知识基底（substrate）

信息整合引擎的核心资产。所有来源渠道的信息归一化成**信息项（item）**落地到这里，
所有消费端（digest 推送 / RAG 问答 / 语料导出）**只读这一层**，不直接接触来源。

```
kb/
├── schema/            权威契约（JSON Schema）
│   ├── item.schema.json       信息项结构
│   └── entity.schema.json     实体结构
├── entities/          实体注册表（有界闭集，人工维护）
│   ├── codecs.yaml            编解码标准    codec:*
│   ├── orgs.yaml              组织          org:*
│   ├── implementations.yaml   实现/研究模型  impl:*
│   ├── datasets.yaml          数据集        dataset:*
│   ├── metrics.yaml           指标          metric:*
│   └── concepts.yaml          技术概念      concept:*
├── items/             信息项（按 type 分目录，如 items/papers/）
└── README.md          本文件
```

## 领域分类（domain × research_line 两层）

音视频技术远不止视频编码。`domain` 是大类（检索口径与优先级按它划分），`research_lines`
是核心域内的细分主线。**video_image_coding 是本引擎的核心域**（深读资源优先），其余域
v1 以 summary 级跟踪、积累实体与信号。

| domain | 覆盖 | v1 深度 |
|---|---|---|
| `video_image_coding` | 视频/图像编码：标准编码器优化、学习式编码、生成式压缩、INR、ICM、部署 | **核心**：deep_read + 精读笔记 |
| `audio_coding` | 音频/语音编码：IAMF、Opus/EVS、神经音频编码 | summary 跟踪 |
| `streaming_delivery` | 流媒体与传输：DASH/HLS/CMAF、WebRTC、ABR、低延迟 | summary 跟踪 |
| `quality_assessment` | 质量评估：IQA/VQA、无参考、QoE 主观实验 | summary 跟踪 |
| `processing_enhancement` | 编码链路处理与增强：超分/去噪/HDR/后滤波 | summary 跟踪 |
| `immersive_media` | 沉浸式与三维：点云压缩、NeRF/3DGS、光场、VR/AR | summary 跟踪 |
| `standards_ecosystem` | 标准进程、专利池、许可、产业政策 | summary 跟踪 |
| `self_improvement` | 自我改进 AI：RSI（递归自我改进）、EoH/FunSearch/AlphaEvolve 式启发式进化、LLM agent 自改进 | summary 跟踪（与核心域交叉的 AI-for-Codec 工作仍归核心域） |

## 设计原则

1. **item 是原子，不是文档**。`docs/` 里的精读笔记是长文形态；item 是同一信息打碎后的
   结构化沉淀（挂实体、拆论断、记指标口径）。两者通过 `summaries.deep_dive` 互链：
   推送读 one_liner，问答读 claims+abstract，深读跳转长文。
2. **claims 是引擎与普通摘要的分水岭**。每条论断带量化指标与口径（scope），
   没有口径的数字不可入库。`confidence` 区分转述（reported）/复测（verified）/推断（inferred）。
3. **实体闭集是精度与护城河的来源**。音视频领域的标准/组织/实现/数据集/指标/概念
   撸总共百级，人工可维护。检索过滤（accuracy 层）= 新信息与实体的匹配，而不是全文相似度。
4. **静态关系放注册表，动态挂接放 item**。「VVenC 实现 VVC」是实体间的恒久事实 →
   `entities/implementations.yaml` 的 relations；「本文拿 VVenC 当改造对象」是
   一次性的 → item 的 `entities[].role`。

## ID 规则

| 对象 | 格式 | 示例 |
|---|---|---|
| 信息项 | `{type}:{channel}:{external_id}` | `paper:arxiv:2606.20847` |
| 实体 | `{prefix}:{CanonicalName}` | `impl:VVenC`、`metric:BD-Rate` |
| 实体文件名 | 按 prefix 分文件 | `kb/entities/codecs.yaml` |
| 信息项文件名 | channel 的 external_id 去版本号 | `kb/items/papers/2606.20847.yaml` |

arXiv 出新版本时**更新原 item**（external_id 记版本、time.updated 记日期），不另开文件。

## 词表（改动 = schema 变更，需同步 schema/*.json）

**item.type**：`paper | standard_proposal | standard_update | repo_release | blog |
benchmark_report | patent | industry_news | dataset_release`

**entities[].role**（item→实体挂接方式）：
`subject`（研究对象）· `uses` · `builds_on`（基于的模型/工作）· `evaluated_on`（数据集）·
`measured_by`（指标）· `compared_against`（对比锚点）· `affiliation` · `platform`（硬件平台）

**relations[].type**（item→item）：事实性 `cites | builds_on | improves_on | compares_with`；
编辑部观察 `same_topic | complements | contrasts_with`（必须带 note 说明观察依据）

**claims[].confidence**：`reported`（转述原文）/ `verified`（本引擎复测）/ `inferred`（多处推断）

**research_lines**：`traditional_codec_opt | learned_codec | coding_for_machines |
generative_compression | inr_representation | systems_deployment`

## 新增一条信息的流程（检索 adapter 的目标形态）

1. 抓取候选 → 判定 `type`，起 `id`；
2. **实体对齐**：标题/摘要与实体注册表的 name+aliases 匹配，挂 entities；
3. **精度过滤**：填 `assessment`（relevance/decision/reason/reviewer）——
   这是「检索精度」落库的地方，被 skip 的不写入；
4. 提炼 claims（带 scope 口径）+ summaries（one_liner_zh 必填）；
5. `uv run --with pyyaml python scripts/validate_kb.py` 通过后才算入库。

新实体（论文提出的新模型等）先补进 `entities/`（research_model + `proposed_in` 回指），
再写 item。

## 校验

```bash
uv run --with pyyaml python scripts/validate_kb.py
```

检查项：必填字段、ID 规则与前后缀一致、实体/指标/关系引用可解析、
`deep_dive` 路径存在、日期格式、全部词表枚举。

## 当前规模

- 实体 90 个（codec 7 / org 21 / impl 25 / dataset 7 / metric 14 / concept 16）
- 信息项 35 个（6 篇手工精读回填 + 29 篇 pipeline 自动审阅；135 条论断 / 111 处量化指标）
