# IQA · 实体档案

> concept:IQA · 数据截止 2026-11-16 · 关联 67 条 · glm-5.3

## 档案概览

| 字段 | 内容 |
|---|---|
| 实体ID | concept:IQA |
| 类型 | concept |
| 名称 | Image Quality Assessment（图像质量评估） |
| 别名 | VQA、video quality assessment、quality assessment、no-reference |
| 挂接条目 | 67 条（2021-02 至 2026-11） |
| 领域定位 | 感知质量度量理论与方法，服务于编解码验证、复原/生成模型训练与评测、QoE 监控、临床/工业可用性判定等下游场景 |

IQA 在本档案中呈现为一条横切音视频全栈的基础能力线：既是编解码标准与压缩性能的**验证工具**（JVET、MPEG/JPEG Pleno 对比），又是复原与生成模型的**训练损失与奖励信号**（LPIPS、CLIP-IQA 驱动超分/去雨/蒸馏），也是近年 LMM/RAG 智能体化的**主动研究领域**。

## 关键事实与演进

### 阶段一（2021–2023）：编解码验证与 3D 内容质量评估的扩展期

- **2021-02**：监控人脸超分工作中发现传统无参考 IQA 指标无法捕捉感知改进，NIMA 经 Mean Opinion Rank 验证与人类感知相关性更好（paper:arxiv:2102.03113）。
- **2021-10**：JVET-X0186 对 VVC vs HEVC 在 8K 分辨率下做主观质量评估，为标准感知增益提供验证证据（standard_proposal:jvet:m188-X0186）。
- **2022-02**：DASH 流媒体 QoE 综述：混合模型（QoS+信号保真度）优于纯 QoS 方法，机器学习模型略优，但现有模型整体性能有限、难落地实际系统（paper:arxiv:2202.12987）。
- **2023**：IQA 向 3D 内容扩展——
  - 静态网格：TSMD（42 参考网格、210 失真样本、74 人 MOS），SOTA 客观指标与 MOS 的 Pearson/Spearman 仅约 0.75（paper:arxiv:2308.01940）；SJTU-TMQA（21 参考、945 失真样本），13 种客观指标最高相关仅约 0.6（paper:arxiv:2309.15675）。
  - 体积视频：全流程综述指出端到端各环节仍存在大量待研究方向（paper:arxiv:2309.05658）。

### 阶段二（2024）：基准化与生成内容质量兴起

- **2024-02**：首次以两种主观协议对比 MPEG 与 JPEG Pleno 点云压缩的感知性能，基于客观指标定义 3 种码率分配策略×4 档码率（paper:arxiv:2402.04760）。
- **2024-07**：Explicit-NeRF-QA（22 物体×4 模型×5 压缩级，21 人 MOS）：全参考指标最优 Pearson 约 0.85，无参考指标仅 0.4–0.6（paper:arxiv:2407.08165）。
- **2024-08**：AIM 2024 压缩视频 VQA 挑战赛：459 条测试视频覆盖 14 种编解码器（H.264/265/AV1/VVC），训练集 CVQAD 1022 条（paper:arxiv:2408.11982）。
- **2024-10**：AIGC 质量综述指出：现有 IQA/VQA 以“重建保真度”为设计目标，不适合生成式伪影；新指标受限于数据集规模小、缺乏代表性（paper:arxiv:2410.08534）。

### 阶段三（2025–2026）：LMM/智能体化与多粒度可解释化

**LMM 驱动的新范式密集涌现**：
- MLLM 驱动 IQA 表征复合退化用于图像修复（paper:arxiv:2601.02763）；免训练 RAG 检索带 MOS 的参考图提升 LMM 零样本 IQA（paper:arxiv:2601.05741；QualiRAG paper:arxiv:2601.18195）；失真感知 VLM + MoE 融合在五个 BIQA 基准超越现有方法（paper:arxiv:2602.09531）。
- 多粒度可解释：IQA-Spider 统一推理/像素定位/区域指涉（paper:arxiv:2605.24553）；VQA 显式区域表示 QRH（paper:arxiv:2610.36978）；GMC 相关曲面揭示全局指标（PLCC/SRCC）对质量分布敏感、模型比较不稳定（paper:arxiv:2601.21738）。
- 智能体化：PACE 免训练多智能体框架将开放式 IQA 整体偏置率从 44.4% 降至 8.6%，每维度仅需 4 张人工标注校准（paper:arxiv:2609.22942）。

**基准与标签方法创新**：
- SR-Prominence：重标注发现 DeSRA 实验室二值伪影中 48.2% 未被多数观看者察觉；SSIM/DISTS 对局部伪影显著度有强预测信号（paper:arxiv:2605.14847）；SR-Ground 63,000 张图像、6 类伪影像素级标注、1,062 人众包验证（paper:arxiv:2605.21244）。
- FoMo：用扩散生成分叉时刻自动生成无人工标注的感知距离标签，训练出的 IQA 度量优于人工标注数据训练版本（paper:arxiv:2609.25716）。
- HVEval+：最大 AI 生成人像视频数据集（1k 提示×24 模型×20k 视频、60k MOS/偏好对），配套 MoE-Rater 统一打分/比较/问答（paper:arxiv:2607.16742）；WorldJen 以 VLM Likert 问卷替代二值 VQA，独立复现人类三层级 BT 结构（Spearman ρ̂=1.000）（paper:arxiv:2605.03475）。

**3DGS/辐射场质量评估成为新热点**：3DGS 视频质量评估框架（paper:arxiv:2507.14454）、SpatialQ 结构感知质量理解（paper:arxiv:2607.26595）、3DGS-IEval-15K+（15,200 图像、45,600 三维 MOS）与 3DGSI-Assessor（paper:arxiv:2608.03279）、参数域全参考指标 GS-PQM 优于 25 种现有指标且免渲染（paper:arxiv:2610.00195）、场景流形方法 SCODA（paper:arxiv:2609.07346）。

**领域专用 IQA 分化**：
- 超声：TinyUSFM-uLPIPS/NRQ 使专家偏好预测准确率从 47.2% 提升至 72.8%（paper:arxiv:2604.19512）。
- 医学影像：LGE-MRI 临床可用性 VLM 判定达 kappa=1.00（paper:arxiv:2608.21180）；测量感知 MLLM 在 LDCT-IQA 2023 追平挑战赛冠军（2.735）（paper:arxiv:2611.08754）；胸片研究中 SSIM/PSNR 常与专家诊断可用性判断不一致（paper:arxiv:2607.26333）。
- 工业/垂直场景：无人机（ICME 2026 第二名，paper:arxiv:2607.00416）、低照度增强（QoMEX 2026 第二名，paper:arxiv:2606.29752）、铁路目标区域质量（paper:arxiv:2611.06203）、海事能见度（常规 IQA 指标无法建立物理可解释关系，paper:arxiv:2606.30049）、织物计数任务型 IQA（最优方法误差仍约 25%，超 ±5% 允差，paper:arxiv:2611.13200）、科研图表评分（paper:arxiv:2607.27066）、超透镜排序省约 80% 成对标注（paper:arxiv:2605.29212）。
- ISP：单帧无参考代理参考图估计 PSNR/SSIM/LPIPS，优于直接指标回归（paper:arxiv:2607.23321）。
- 语音侧映射：UTMOS 保分/保质攻击暴露评分与真实质量脱钩（paper:arxiv:2606.31105）。

**作为训练/评测基础设施持续被消费**：
- 训练侧：IQA 动态奖励驱动无配对去雨（paper:arxiv:2605.00719）；指标引导动态损失控制器 DLC 平衡保真与感知（paper:arxiv:2610.11433）；无参考质量目标引导递归超分（paper:arxiv:2609.06490）；BlindPSNR 无参考预测 PSNR 使 LLIE 参数选择精度从 54.4% 升至 89.5%（paper:arxiv:2607.27628）。
- 评测侧：4K/UHD 主观实验（216 序列、30 人）表明 VMAF/PSNR 对神经编解码器仍有效，FasterVQA 为最佳无参考指标（paper:arxiv:2511.00969）；扩散式 VSR 上 CNN 全参考模型（LPIPS/DISTS/CVQA-FR）显著优于传统与无参考模型，但均不足以替代主观测试，VMAF 因空间不一致性失效（paper:arxiv:2605.25940）；SI-PSNR 惩罚过锐化，锐度感知损失图像获 67% 主观偏好（paper:arxiv:2608.13989）；VHA/VHA+ 评估生成式超分幻觉（paper:arxiv:2610.25770）。
- 挑战赛评测协议结合 IQA 与效率：NTIRE 2026 移动端 SR 以 IQA 得分×加速比加权排名，108 注册/16 有效队（paper:arxiv:2604.17306）。
- 其他量化锚点：SparkVSR CLIP-IQA 最高 +24.6%（paper:arxiv:2603.16864）；5G FWA 实测 VMAF 与网络条件帧级关联（paper:arxiv:2609.25423）；TTA 统一免参考 VQA 与超分（paper:arxiv:2608.08508）；VIGIL-140K 失真检测训练集（paper:arxiv:2608.09122）；ReLIQS 分辨率无关无参考 IQA（paper:arxiv:2608.01730）；自编码器潜空间余弦相似度替代 PSNR/SSIM（paper:arxiv:2608.24782）；PCH 立体全景盲评估（paper:arxiv:2608.28798）；Undertone 少样本个性化美学评判（paper:arxiv:2609.27110）；ClearAIR/ClearGS/EORestore-Agent/Robust-U1/Fill2SR/MV-SDI/CogCanvas 等以 IQA 指标作为验收标准（paper:arxiv:2601.02763, 2609.31509, 2610.06196, 2606.08063, 2609.33582, 2606.29964, 2606.15867）。

## 当前状态与关注点

**活跃度**：极高。2026 年挂接条目约 40 条，占总量近六成；LMM/MLLM 化、RAG 化、智能体化、可定位/可解释化、AIGC 与 3DGS 评估是当前五条主增长线。

**开放问题**：
1. **AIGC 评估失配**：保真度范式指标不适用于生成式伪影，新指标受限于小数据集与缺失性能测度（paper:arxiv:2410.08534）。
2. **无参考指标性能天花板**：NeRF 数据上 NR 指标 Pearson 仅 0.4–0.6（paper:arxiv:2407.08165）；扩散式 VSR 上无参考模型整体落后于 CNN 全参考模型（paper:arxiv:2605.25940）；七类 NR-IQA 基线在保真度参数选择任务上精度为 0%，暴露“感知质量 vs 信号保真度”的目标分歧（paper:arxiv:2607.27628）。
3. **评估协议本身**：全局标量指标（PLCC/SRCC）对样本质量分布敏感（paper:arxiv:2601.21738）；二值伪影标注高估感知影响（paper:arxiv:2605.14847）；MOS 标注昂贵带噪，自动标签管线（FoMo）开始替代（paper:arxiv:2609.25716）。
4. **鲁棒性与可信度**：UTMOS 类模型可被保分攻击，评分与真实质量脱钩（paper:arxiv:2606.31105）。
5. **任务型 IQA**：图像质量需以“跨复拍的可靠性”而非绝对保真度定义（织物计数复拍差异中位数 9%）（paper:arxiv:2611.13200）。

**生态位**：IQA 处于“被消费的基础设施”与“主动演化的研究领域”双重位置——上游为编解码标准验证（JVET/AOMedia/MPEG/JPEG Pleno）提供感知证据，中间为复原/生成/流媒体模型提供损失与奖励信号，下游则正被 LMM 范式重构为多粒度、可解释、可对话的质量理解能力。〔档案推断〕按当前趋势，AIGC 与 3DGS/辐射场质量评估将延续为主战场，IQA 与质量理解（grounding、reasoning、ranking）的融合会进一步模糊其与多模态理解的边界。
