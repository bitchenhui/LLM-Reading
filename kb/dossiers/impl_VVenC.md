# VVenC · 实体档案

> impl:VVenC · 数据截止 2026-11-16 · 关联 29 条 · glm-5.3

# 实体档案：VVenC（impl:VVenC）

## 档案概览

| 项 | 内容 |
|---|---|
| 实体 | impl:VVenC — Fraunhofer Versatile Video Encoder（别名 VVenC encoder） |
| 类型 | implementation / production_encoder |
| 开发方 | org:Fraunhofer-HHI |
| 标准关系 | implements → codec:VVC（ITU-T H.266 / ISO/IEC 23090-3，2020-07 定稿） |
| 注册表定位 | VVC 主流开源实现；fast/RDO 优化的最常见宿主（注册表备注点名 paper:arxiv:2606.20847、paper:arxiv:2606.31084 两篇为本库重点改造案例） |

**档案构成（29 条，跨度 2021-07 → 2026-09）**：
- 版本发布 11 条：VVenC 自 v1.12.0-rc2（2024-06）至 v1.14.0（2026-01）共 10 条，另挂关联解码器 VVdeC v3.0.0 一条；
- 论文 10 篇：VVenC 作为研究对象、工具链组件或竞品基线；
- JVET 提案 8 篇：HHI 例行进展汇报（m188–m195，2021-10 → 2023-07）。

档案呈**双轨叙事**：工程线（版本演进 + JVET 汇报）与研究线（外部学术改造）并行，2026 年研究侧热度显著抬升（单年 6 篇）。

## 关键事实与演进

### 2021：诞生与开源端到端闭环
- VVC 于 2020-07 定稿，相同主观质量下较 HEVC 约省 50% 码率（条目口径；正文另载独立主观验证中 HD/UHD 平均节省超 40%）[paper:arxiv:2107.13385]。
- 首发论文即完成生态闭环：VVenC 编码 + VVdeC 解码 + GPAC/FFmpeg 封装 + DASH 传输，在标准定稿一年后即可搭建覆盖编码、封装、自适应流与播放的全流程工具链，并附文件播放与 DASH 两个分步教程 [paper:arxiv:2107.13385]。
- 2021-10 JVET-X0044 开启向 JVET 的进展汇报线 [standard_proposal:jvet:m188-X0044]。

### 2022 – 2023.07：JVET 例行汇报与能力扩展
- 例行更新序列：Y0136（2022-01）[standard_proposal:jvet:m189-Y0136]、AA0154（2022-07）[standard_proposal:jvet:m191-AA0154]、AB0044（2022-10）[standard_proposal:jvet:m192-AB0044]、AC0266（2023-01）[standard_proposal:jvet:m193-AC0266]、AD0266（2023-04）[standard_proposal:jvet:m194-AD0266]、AE0266（2023-07）[standard_proposal:jvet:m195-AE0266]；档案内无 2022-04（m190）届条目〔档案推断：属采集空档而非项目中断〕。
- 专题里程碑：AE0172（2023-07）单独汇报**多层（分层/可分级）编码**支持的实现进展，是档案内唯一非例行性的 VVenC 技术提案 [standard_proposal:jvet:m195-AE0172]。

### 2023 – 2024：作为学术改造宿主的第一波
- **两遍码控第一遍替换**：低复杂度视频特征 + 随机森林替代 VVenC 全帧内两遍码控第一遍，faster 档编码时间 **-32%**、BD-rate **+2%**、码控精度相当 [paper:arxiv:2306.16786]。
- **多码率编码加速**：以最低码率表征为参考复用划分图，从属表征编码时间平均 **-40%**、VMAF 平均仅降 **0.43**，且与并行编码兼容 [paper:arxiv:2312.08330]。
- **竞争数据点**：MPEG MIV CTC 下，INR 编码器 MV-HiNeRV 相对内置 VVenC 的 TMIV 最高 BD-rate 节省 **72.33%**（论文自报，多视点纹理+深度场景）[paper:arxiv:2402.01596]。

### 2024-06 – 2026-01：工程演进主线（v1.12 → v1.14）

| 版本 | 日期 | 关键变更 |
|---|---|---|
| v1.12.0 | 2024-06 | 新增 **CQF 封顶恒定质量模式**（固定 QP + QPA + 最大码率约束时生效）；simple app 支持单色视频；多线程自动配置（simple 默认开 / FF-app 默认关，mtprofile 可禁用，**编码结果随线程数变化**）；faster 档提速 ~5% [repo_release:github:vvenc-v1.12.0]（rc2 同步见 [repo_release:github:vvenc-v1.12.0-rc2]） |
| v1.12.1 | 2024-10 | VUI 标志改为**符合 DVB 规范**（广播码流一致性）；开放更多 VUI 标志命令行控制 [repo_release:github:vvenc-v1.12.1] |
| v1.13.0 | 2024-12 | 多项 ARM 平台优化；**实验性胶片颗粒分析（FGA）**；medium 档提速 5% 并降低内存；DASH 优化刷新模式 **idr_no_radl**；GOP 自适应 QP 级联（仅非 QPA）[repo_release:github:vvenc-v1.13.0] |
| v1.13.1 | 2025-03 | x86 最低指令集升至 **SSE 4.1**；修复旧 x86 非法指令、slice type adaptation 下码控精度退化、ARM 非对齐 load/store、32 位 ARM SIMD 水平加法、FGA 行/列访问；新增可选帧级用户数据 API 扩展 [repo_release:github:vvenc-v1.13.1] |
| v1.14.0 | 2026-01 | 大量 ARM **NEON/SVE** 优化，硬件支持时默认启用 SVE；API 变更：vvenc.h 中 cts/dts 改有符号整数；**弃用 LMCS**（未来版本移除）；静态链接不再需要 nlohmann_json（捆绑版升至 3.12.0）[repo_release:github:vvenc-v1.14.0] |

- 生态侧证：VVdeC v3.0.0（2024-10）为破坏性 API 版本，新增胶片颗粒支持，并**移植 VVenC 的外部 ARM SIMD 优化**——VVenC 是 HHI 编解码双件套中的 SIMD 优化上游 [repo_release:github:vvdec-v3.0.0]。

### 2026：研究热点集中爆发（码控 × 流媒体 × LLM）
- **易用性层 / LLM 命令生成**：ELLMPEG 边缘代理式 LLM 框架自动生成并本地校验 FFmpeg/VVenC 命令；Qwen2.5 + 框架平均命令生成准确率 **78%**、零经常性 API 成本；构建 **480 条**提示数据集，按有效性/tokens/时延/能耗评测 4 个开源 LLM [paper:arxiv:2602.00028]。
- **两遍码控第二击**：VCA 轻量特征 + QP 经随机森林预测帧级比特（UHD、VVenC 编码，I/P/B 帧 R² = **0.93 / 0.88 / 0.77**），嵌入码控回路后效率与 VVenC 2pRC 相当、总编码时间 **-33.3%**，可避免 2pRC 的多次试验编码 [paper:arxiv:2602.06242]。
- **流媒体组件**：DQ-Ladder 深度强化学习码率阶梯以 VVenC/VVdeC 为工具链，较 Apple HLS 阶梯 XPSNR BD-rate 至少 **-10.3%**、解码时间 **-22%**（VVdeC 解码；750 序列 × 6 分辨率 × 41 QP）[paper:arxiv:2603.13597]。
- **LLM 设计编码器启发式**（注册表点名改造对象 ①）：DeepSeek 闭环进化（种群 K=4、10 轮）自动发现帧级 QP 启发式，等价于「熵约束 RDO」（score = weighted_PSNR/(1+H_QP)/log(1+total_bits)）；相对 **VVenC-1.7.0** faster 固定 QP（RA）：CTC B 类 BD-rate **-1.73%**（YUV-PSNR）、UVG **-1.00%**、MCL-JCV **-1.06%**，三库总平均约省 1.26% 码率 [paper:arxiv:2606.20847]。
- **工具级快速算法**（注册表点名改造对象 ②）：2-tap 滤波器差分近似把 8-tap 分数插值下的 MMVD 候选判决（4 方向 × 8 距离，60–80% 尝试耗于 1/4 pel 精度）降为一次残差-梯度内积符号判断；MMVD 搜索占比 **21%→11%**、η **11.79→7.10**；fast 档 +Ours：BD-rate **-0.35%** / 时间节省 **2.23%**（对照基线 -0.64% / 21.10%），faster 档 **-0.72% / 4.64%**（基线时间节省 36.39%）；条目自评为「几乎不损失压缩率地拿走大部分加速收益」[paper:arxiv:2606.31084]。
- **LLM 设计编码工具的递进**：生成-评估闭环产出 Planar 预测器，VVenC faster 下替换默认 Planar 省码率 **0.18%**、复杂度 **+0.4%**；并验证向 ECM 的两种集成策略（直接替换方向性 Planar / 作为带新语法元素的附加模式）在受限低分辨率下均有增益。该文明确将 2606.20847 的 QP 规则定位为「预编码阶段、与核心流水线松耦合」，本文将范式推进至编码工具本体 [paper:arxiv:2609.01535]。

## 当前状态与关注点

### 活跃度
- **发布节奏稳定**：2024 年起每年约两个 minor 版本（1.12 → 1.13 → 1.14），rc1 至正式版间隔约一周；档案内最新为 v1.14.0（2026-01-21）[repo_release:github:vvenc-v1.14.0]。
- **研究牵引持续增强**：2026 年 1–9 月已有 6 篇论文以 VVenC 为宿主或组件（命令生成、码控、码率阶梯、LLM 启发式、MMVD 快速算法、LLM 工具设计），为档案内单年峰值。
- JVET 汇报线在档案内止于 2023-07 [standard_proposal:jvet:m195-AE0266]〔档案推断：更可能反映本库采集范围收口，而非项目退出 JVET 汇报，待补证〕。

### 开放问题
- **LMCS 弃用**（v1.14.0 起，未来移除）：依赖 LMCS 的存量工作流迁移影响在档案内无记录 [repo_release:github:vvenc-v1.14.0]。
- **可复现性约束叠加**：cts/dts 有符号化 API 变更（v1.14.0）、x86 最低要求升至 SSE 4.1（v1.13.1）、多线程自动配置下「编码结果随线程数变化」（v1.12.0）三者并存，对结果确定性敏感的研究与生产流程构成工程约束 [对应版本条目]。
- **研究版本滞后**：2606.20847 实验基于 VVenC-1.7.0，而同期发行版已至 1.14.0——学术结论向现行版本的迁移成本与可比性是隐性风险〔档案推断〕。
- **两遍码控成本是被反复攻克的外部痛点**（全帧内第一遍替换 -32% [paper:arxiv:2306.16786]；帧级比特预测替代 2pRC -33.3% [paper:arxiv:2602.06242]），但档案内均无上游合入记录〔档案推断〕。

### 生态位
- **VVC 开源生态双核之一**：与 VVdeC 配对构成 HHI 工具链，且为 SIMD 优化的上游源（ARM 优化被 VVdeC v3.0.0 反向移植）[repo_release:github:vvdec-v3.0.0]；经 FFmpeg/GPAC/DASH 融入通用流媒体栈 [paper:arxiv:2107.13385]。
- **场景覆盖持续外扩**：广播（DVB VUI 合规 [repo_release:github:vvenc-v1.12.1]）、DASH 流媒体（idr_no_radl、CQF 封顶质量、多码率与阶梯研究 [repo_release:github:vvenc-v1.13.0][paper:arxiv:2312.08330][paper:arxiv:2603.13597]）、移动/嵌入式（ARM NEON/SVE 默认化 [repo_release:github:vvenc-v1.14.0]）、多层/可分级 [standard_proposal:jvet:m195-AE0172]。
- **LLM 时代的双重角色**：既是 LLM 生成命令的操作对象（ELLMPEG [paper:arxiv:2602.00028]），又是 LLM 自动设计编码启发式/工具的实验平台（QP 规则、Planar 预测器 [paper:arxiv:2606.20847][paper:arxiv:2609.01535]）；后者已验证可向 ECM 迁移，提示研究前沿载体正酝酿向 VVenC 之外扩展。
- **竞争压力记录在案**：沉浸式/多视点子领域，INR 方案 MV-HiNeRV 相对内置 VVenC 的 TMIV 最高 72.33% BD-rate 节省（论文自报、单点数据）[paper:arxiv:2402.01596]——传统混合编码器在神经方法强势场景的边界值得持续追踪。
