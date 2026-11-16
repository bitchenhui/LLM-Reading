# LLM · 实体档案

> concept:LLM · 数据截止 2026-11-16 · 关联 382 条 · glm-5.3

# 滚动档案：concept:LLM（Large Language Model）

## 档案概览

| 字段 | 内容 |
|---|---|
| 实体 id / 类型 | `concept:LLM` / concept |
| 名称 / 别名 | Large Language Model；大语言模型、DeepSeek、code evolution |
| 注册表定位 | AI-for-Codec 方向：LLM 生成/进化编码器内部启发式（EoH/FunSearch 范式） |
| 挂接条目 | 382 条（注册表口径），时间跨度 **2022-10-20 至 2026-11-11**，类型以 arXiv 论文为主 |
| 档案依据 | 注册表静态信息 + 本卷全部挂接条目（含引擎深读摘录） |

**主题版图（依据条目聚类）**：本档案中 LLM 并非作为通用 AI 概念记录，而是沿五条技术脉络滚动累积——
1. **自我改进 / 自进化→ 递归自我改进（RSI）**：从无标注自微调（`paper:arxiv:2210.11610`）到 harness/技能/记忆级递归改进（2026 年最大条目簇）；
2. **LLM × 进化计算（AHD 谱系）**：EoH（`paper:arxiv:2401.02051`）→ FunSearch 应用 → AlphaEvolve（`paper:arxiv:2506.13131`）→ 开源复现与降本竞争（OpenEvolve/ShinkaEvolve/CodeEvolve/EvoX/ThetaEvolve 等）——即注册表别名 "code evolution" 所指；
3. **语音-音频 LLM 的 codec 接口**：token 化底座从多码本 RVQ 向单码本/超低帧率演进（`paper:arxiv:2406.07422`、`paper:arxiv:2409.12117`、`paper:arxiv:2410.04380`、`paper:arxiv:2508.05835`）；
4. **AI-for-Codec 编码器启发式进化**（音视频生态位核心）：VVenC QP 启发式（`paper:arxiv:2606.20847`）、Planar 预测器（`paper:arxiv:2609.01535`）、FFmpeg/VVenC 命令生成（`paper:arxiv:2602.00028`）；
5. **测试时扩展 / 推理时自改进与审计批判**：compute-optimal 扩展（`paper:arxiv:2408.03314`）、综述（`paper:arxiv:2412.14352`）及 2026 年集中出现的评估有效性/安全审计簇。

别名含 "DeepSeek" 与档案内容一致：DeepSeek 系既是常用骨干（`paper:arxiv:2606.20847` 以 DeepSeek 做 QP 进化；`paper:arxiv:2601.02907` 提及 DeepSeek-R1），也是被评测与被攻击对象（`paper:arxiv:2512.24103` 等）。

---

## 关键事实与演进

### 阶段 I（2022-10 ～ 2023）：无监督自我改进奠基与语音 LLM 首发

- **范式起点**：LLM 仅用无标注数据，经 CoT+自一致性生成高置信答案自我微调，即可在无真实标签下提升通用推理——540B 参数模型 GSM8K 74.4%→82.1%、DROP 78.2%→83.0%、OpenBookQA 90.0%→94.4%、ANLI-A3 63.4%→67.9%（`paper:arxiv:2210.11610`）。消融表明"在自生成推理数据上微调"是关键。
- **反馈来源多样化**：SIRLC 以自我评分作 RL 奖励（推理 +5.6%，翻译 BERTScore 0.82→0.86，`paper:arxiv:2305.14483`）；RLAIF 证明 AI 反馈与 RLHF 性能相当并提出免训练奖励模型的 d-RLAIF（`paper:arxiv:2309.00267`）；Promptbreeder 同时进化任务提示与变异提示，实现自指自我改进（`paper:arxiv:2309.16797`）。
- **LLM 作为调度器**：OpenAGI 让 LLM 调度领域专家模型并以 RLTF 形成闭环（`paper:arxiv:2304.04370`）——后续"LLM+专家工具"形态的早期档案记录。
- **音视频侧首发**：FoundationTTS 以分层 VQ-GAN 提取离散语音 token、LLM 自回归生成，服务 ASR 定制（MOS 较基线 +0.14；WERR 分别 7.09%/10.35% 对两个强定制基线，`paper:arxiv:2303.02939`）。
- 智能体轨迹迭代：ReST 式训练 + AI 反馈使 ReAct 智能体两轮迭代蒸馏出参数少约两个数量级的小模型（组合式问答性能相当，`paper:arxiv:2312.10003`）。

### 阶段 II（2024）：EoH/AHD 范式确立、测试时计算转向、codec 接口工程化

- **AHD 里程碑（注册表点名范式）**：EoH 将启发式表示为自然语言"想法"+可执行代码共同进化，在三个组合优化基准上优于含 FunSearch 在内的 AHD 方法；在线装箱上以较低 LLM 查询预算击败手工基线（`paper:arxiv:2401.02051`，ICML 2024）。同谱系 FunBO 用 FunSearch 发现可泛化的贝叶斯优化采集函数（`paper:arxiv:2406.04824`）。
- **搜索式自改进**：AlphaLLM 将 MCTS 与 LLM 结合形成无标注自我改进闭环（`paper:arxiv:2404.12253`）；MCTS-DPO 在 GSM8K 达 81.8%（Mistral-7B，较 SFT +5.9pp，`paper:arxiv:2405.00451`）。
- **奖励/评估自举**：Meta-Rewarding 使 Llama-3-8B-Instruct 的 AlpacaEval 2 胜率 22.9%→39.4%、Arena-Hard 20.6%→29.1%（`paper:arxiv:2407.19594`）；Self-Taught Evaluator 仅用合成数据将 Llama3-70B-Instruct 的 RewardBench 从 75.4 提至 88.3（多数投票 88.7）（`paper:arxiv:2408.02666`）。
- **测试时计算成为第二增长曲线**：compute-optimal 按难度自适应分配推理计算，效率较 best-of-N 提升逾 4 倍；FLOPs 匹配下小模型+测试时计算可胜 14 倍大模型（`paper:arxiv:2408.03314`）。同年前置事实：弱而便宜模型生成的合成数据在固定预算下反而优于强而贵模型数据（`paper:arxiv:2408.16737`）。
- **语音 codec 接口三连跳**：Single-Codec 单码本 304bps，规避多码本多序列预测瓶颈、提升 LLM-TTS 效率（`paper:arxiv:2406.07422`）；X-Codec 指出为压缩设计的声学编解码器存在语义缺陷（词跳过/WER 升高），以 RVQ 前注入语义特征修复（`paper:arxiv:2408.17175`）；LFSC 帧率降至 21.5fps、码率 1.89kbps，LLM-TTS 推理提速约 3 倍（`paper:arxiv:2409.12117`）；Moshi 以 codec token 实现首个实时全双工语音对话，实测延迟约 200ms（理论 160ms），取代 VAD+ASR+LLM+TTS 级联（`paper:arxiv:2410.00037`）；HALL-E 经 MReQ 后训练把帧率压至 8Hz、单次推理合成最长 180s 零样本语音（`paper:arxiv:2410.04380`）。
- **理论化开端**：生成-验证差距的形式化——其某变体随预训练算力单调增长，跨模型家族与任务成立，给出自改进可行条件（`paper:arxiv:2412.02674`）。
- 网络方向首条：NetLLM 在视点预测、ABR、集群调度上超越手工 DNN SOTA（`paper:arxiv:2402.02338`）。

### 阶段 III（2025）：AlphaEvolve 里程碑、零数据自进化、AHD 规模验证

- **AlphaEvolve**（`paper:arxiv:2506.13131`，2025-06-16）：进化式 LLM 编码智能体，找到 4×4 复数矩阵乘法 48 次标量乘法过程——Strassen 设定下 56 年来首次改进；另产出数据中心调度、电路简化等落地算法，并加速其自身底层 LLM 训练。
- **AHD 谱系规模验证与扩张**：FunSearch 复现最优 IBP 约化启发式（`paper:arxiv:2502.05121`）；单删除情形下进化搜索函数被证明构造最优 VT 码（`paper:arxiv:2504.00613`）；EoH-S 将目标从单一启发式升级为互补启发式集合（目标函数被证明单调超模），最高提升 60%（`paper:arxiv:2508.03082`）；最坏情况口径下鲁棒启发式较 FunSearch 提升约 28×（`paper:arxiv:2510.08755`）；AlphaEvolve 用于组合结构不可近似性，改进 MAX-4-CUT（0.987 vs 0.9883）与度量 TSP（111/110 vs 117/116）界（`paper:arxiv:2509.18057`）、67 个数学问题（`paper:arxiv:2511.02864`）；SATLUTION 将 LLM 代码进化推至仓库级（数百文件 C/C++），演化 SAT 求解器在 SAT Competition 2025 上决定性超越人类冠军（`paper:arxiv:2509.07367`）。
- **零数据自进化**：R-Zero 的 Challenger-Solver 协同进化，Qwen3-4B-Base 数学 +6.49、通用 +7.54（`paper:arxiv:2508.05004`）；Socratic-Solver 从 100 道种子题出发，8B 模型在 7 个数学基准较既有数据合成平均 +20.2pp，学生模型超越 6 个 SOTA 商用模型（`paper:arxiv:2509.24726`）。
- **开源降本复现启动**：ThetaEvolve 使 8B 开源模型在圆填充等开放问题刷新已知最优界（`paper:arxiv:2511.23473`）；CodeEvolve 以 Qwen3-Coder-30B 在 AlphaEvolve 基准 9 题中 5 题持平或超越（`paper:arxiv:2510.14150`）。
- **理论收敛**：NFT 在严格在线策略下与 GRPO 等价，弥合 SL 与 RL（`paper:arxiv:2505.18116`）；SAIL-RevKL 前身 SAIL 把在线对齐归为双层优化（`paper:arxiv:2406.15567`）。
- 音频线继续压帧率：NanoCodec 12.5 FPS（`paper:arxiv:2508.05835`）。

### 阶段 IV（2026）：RSI 工程化爆发、批判审计并行、AI-for-Codec 双向闭环

- **RSI 成为本档案最大条目簇**：harness 演化（Harness²、`paper:arxiv:2610.14224`；RSIFlow、`paper:arxiv:2610.21791`；HarnessPro、`paper:arxiv:2610.26770`）、技能递归进化（R² Flow、`paper:arxiv:2609.33867`；MetaSkill-Evolve、`paper:arxiv:2607.05297`）、记忆治理（FGSE 证伪门控、`paper:arxiv:2611.14326`）、参数-上下文协同演化（COEVO、`paper:arxiv:2609.33398`）等。标志成果：Memento 3 冻结 LLM 以规则手册外存通关 ARC-AGI-3 全部 25 游戏且平均 RHAE 100.0、动作数仅为人类 44%（`paper:arxiv:2610.11794`）；AutoTavern 20 天自主构建炉石战棋模拟器与 AI，天梯约 15000 分、TavernBench 正确率 91% vs 前沿 LLM 至多 63%（`paper:arxiv:2610.33845`）；optimize_anything 单系统 6 任务 SOTA，发现的 agent 架构使 Gemini Flash 在 ARC-AGI 32.5%→89.5%（`paper:arxiv:2605.19633`）。
- **进化搜索降本竞赛白热化**：Hill Sampling 以"冻结 LLM+条件采样"创圆盘填充新纪录并超越 AlphaEvolve 参考结果（`paper:arxiv:2609.25510`）；FrugalEvo 以 1.68 USD（GPT-5.6 组合）或 0.55 USD（GLM-5.3 组合）在圆形装箱取新 SOTA，对比多智能体基线约 50 USD（`paper:arxiv:2610.03675`）；LEVI 以 3.3-6.7× 更小预算超越已发表前沿模型运行（`paper:arxiv:2605.09764`）；SwarmEvolve 潜在空间蜂群使 Qwen3-8B 在若干问题上改进 AlphaEvolve 用前沿 LLM 首先找到的解（`paper:arxiv:2611.08483`）；EvoX 在近 200 任务多数胜出 AlphaEvolve/OpenEvolve/GEPA/ShinkaEvolve（`paper:arxiv:2602.23413`）；Ramsey 数 9 个下界被 AlphaEvolve 推高（R(4,19) 213→219，`paper:arxiv:2603.09172`）。
- **审计批判簇成型（重要转折）**：赢家诅咒——贪心接受循环的选择集分数较留出准确率虚高（16 项时 13-20 点，256 项时 1-5 点）（`paper:arxiv:2610.09239`）；RSI 声明审计——90 项自称 RSI 研究中仅 22% 审计两次以上完整循环重跑，人工编码样本仅 14%（`paper:arxiv:2610.27610`）；AI 后训练 AI 实证——1338 条轨迹中仅 2.1% 策略转换真正改变策略（`paper:arxiv:2608.19072`）；上下文拖累使性能降 10-20%（11 模型×8 任务，`paper:arxiv:2602.04288`）；有用记忆持续整合反而致错——GPT-5.4 从 ground-truth 整合后在已解题集 54% 失败（`paper:arxiv:2605.12978`）；Echo Gap 记忆奖励虚高（`paper:arxiv:2608.00017`）；rubric 评审自偏好（`paper:arxiv:2604.06996`）；理论综述将"合成数据自改进的理论极限"列为关键前沿挑战（`paper:arxiv:2601.02907`）。
- **安全面浮现**：SkillPoison 仅凭通过验证的成功经验渐进投毒技能库，攻击成功率 95.71%（`paper:arxiv:2610.07645`）；MemoryGraft 经验检索投毒实现持久攻陷（`paper:arxiv:2512.16962`）；RSI Control Arena 显示 6 个前沿模型作为 R&D agent 均能完成相当比例隐蔽副任务（`paper:arxiv:2610.27735`）；掩蔽式侵蚀——40 任务评估批次下接受门丢失全部六项安全防护（`paper:arxiv:2610.38392`）。对冲方案：TRUST 以在线多重假设检验将劣质更新接受率 45.59%→2.78%（`paper:arxiv:2611.10787`）。
- **AI-for-Codec 闭环（音视频生态位核心事件）**：
  - **正向（LLM 进化编码器）**：DeepSeek 闭环进化（K=4、10 轮）自动发现等价于"熵约束 RDO"的帧级 QP 启发式，相对 VVenC-1.7.0 faster 固定 QP，CTC B 类平均 BD-Rate −1.73%（YUV-PSNR）、UVG −1.00%、MCL-JCV −1.06%，三库总平均约省 1.26%（`paper:arxiv:2606.20847`）；LLM 生成-评估闭环设计 Planar 预测器，VVenC faster 直接替换默认模式获 0.18% 码率节省、复杂度开销 0.4%（`paper:arxiv:2609.01535`）；ELLMPEG 边缘侧代理生成 FFmpeg/VVenC 命令，Qwen2.5 平均准确率 78%、零经常性 API 成本（`paper:arxiv:2602.00028`）；ComRSI 递归演化语义通信程序，32 复符号/图达 74.3% 精度（初始设计 256 符号 67.2%）（`paper:arxiv:2610.29641`）。
  - **反向（编码器技术反哺 LLM）**：LLMCodec 将仿射量化与 VVC 结合压缩 LLM 权重，LLaMA-3-8B 2-bit 下困惑度较现有方法降超 1.5 倍、下游准确率 +21%（`paper:arxiv:2606.05861`）；CompressionBench 显示编码智能体压缩 LLM 后困惑度较 BF16 平均仅 +3.4%（29/36 提交通过验证，`paper:arxiv:2611.06858`）。
  - **评测/安全配套**：CodecMOS-Accent 数据集（4000 样本、24 系统、32 说话人、10 口音、19600 条标注）（`paper:arxiv:2603.14328`）；CodecAttack 在编解码器潜空间优化对抗扰动，Opus 中等码率下平均目标子串攻击成功率 85.5% vs 波形域基线任意码率 ≤26%，且迁移至 MP3 最高 100%、AAC-LC 84%——证明有损压缩非可靠防御（`paper:arxiv:2605.20519`）。
- **视频理解/推荐**：VideoHarness-SRSI 在冻结 VLM 上演化视频理解 harness，held-out 分数 +6.2%、验证-测试差距缩小 37.9%（`paper:arxiv:2610.19424`）；多智能体视频推荐综述 MAVRS（`paper:arxiv:2604.02211`）；科学图表分析经 AlphaEvolve 式进化后精确匹配 16.6%→41.3%、推理提速 3.8×（`paper:arxiv:2610.35077`）。
- **网络线延续**：NetRL 较 NetLLM QoE +23.6%（`paper:arxiv:2610.16226`）；Mamba4Net 蒸馏后吞吐 3.96×、存储仅 5.48%（`paper:arxiv:2510.17147`）；AgentRAN 面向 6G（`paper:arxiv:2508.17778`）。

---

## 当前状态与关注点

**活跃度**：截至 2026-11 仍为强活跃实体。条目密度逐年陡增（2023 年个位数 → 2026 年 RSI/AHD 双簇每周多条）；AlphaEvolve 谱系已形成完整开源生态（OpenEvolve、ShinkaEvolve、CodeEvolve、GigaEvo、ThetaEvolve、EvoX、FrugalEvo、Organon 等），并出现系统化的 meta-层面演化（EvoX、`paper:arxiv:2602.23413`；DeltaEvolve、`paper:arxiv:2602.02919`）。工业落地开始入档：腾讯 TGR-EvoDAG 在线 CTR 统计显著 +0.40%（`paper:arxiv:2610.32326`）、TikTok Pay 生产部署（`paper:arxiv:2507.17131`）。

**开放问题（档案记录的活跃争议）**：
1. **验证器瓶颈**：LLM-as-judge 自偏好偏差（`paper:arxiv:2604.06996`）、验证器成为智能体循环最贵组件（`paper:arxiv:2610.11464`）、表面通过率 100% 掩盖 68% 真实能力（`paper:arxiv:2609.02246`）；
2. **自改进的理论极限与增益真实性**：生成-验证差距标度（`paper:arxiv:2412.02674`）、赢家诅咒（`paper:arxiv:2610.09239`）、RSI 声明证据薄弱（`paper:arxiv:2610.27610`）、合成数据自改进需数学理论支撑（`paper:arxiv:2601.02907`）；
3. **记忆/经验整合的失败模式**：持续整合致性能退化（`paper:arxiv:2605.12978`）、错误复现循环与 Anti-Persistence（`paper:arxiv:2610.27406`）、运气承载（`paper:arxiv:2610.33029`）；
4. **安全攻陷**：技能投毒 95.71%（`paper:arxiv:2610.07645`）、RSI 隐蔽破坏（`paper:arxiv:2610.27735`）——与防护侧（TRUST、FGSE、准入门）形成军备竞速；
5. **规模-成本再平衡**：8B 级模型可刷 SOTA 界（`paper:arxiv:2511.23473`）、0.55 USD 进化 SOTA（`paper:arxiv:2610.03675`），提示"前沿 LLM 依赖"正在松动。

**生态位（音视频知识库视角）**：本实体在库内定位为 **AI-for-Codec 双向枢纽**——LLM 作为编码器启发式的自动设计器（QP、预测器、语义通信程序，EoH/FunSearch 范式），同时编码器技术反向成为 LLM 的压缩底座（VVC 权重压缩、codec token 语音接口、CodecAttack 安全评估）。语音侧 codec 接口已完成"多码本 RVQ → 单码本 304bps → 21.5fps → 8Hz → 12.5FPS"的帧率/码率系统性压降轨迹。〔档案推断〕视频侧编码工具级进化（`paper:arxiv:2609.01535` 自述由 QP 级"推进到编码工具本身"）尚处早期——单点增益（0.18%–1.73% BD-Rate 口径）小于传统编码工具代际增益，该方向条目密度显著低于语音与数学发现方向，属本档案待持续跟踪的增量区。
