# AlphaEvolve · 实体档案

> concept:AlphaEvolve · 数据截止 2026-11-16 · 关联 33 条 · glm-5.3

# 实体档案：AlphaEvolve（concept:AlphaEvolve）

## 档案概览

| 字段 | 内容 |
|---|---|
| 实体 | AlphaEvolve（concept:AlphaEvolve，concept） |
| 定义 | Google 提出的进化式 LLM 编码智能体：以 LLM 为语义感知变异算子，配合确定性评估器打分与程序数据库/档案回填，迭代改写代码以自动发现新算法，是 FunSearch 的工程化扩展 (paper:arxiv:2506.13131) |
| 挂接条目 | 33 条，跨度 2025-06-16 → 2026-11-10 |
| 条目构成 | 原始论文 1 篇；直接应用/领域扩展约 12 篇；开源复现与框架改造约 14 篇；替代范式（测试时训练、流匹配、纯采样）约 4 篇；形式化验证路线 2 篇；能力边界评估 1 篇 |
| 音视频知识库定位 | 非核心上游技术；其「fitness-in-the-loop 程序搜索 + 沙箱评估」范式被认定为可迁移至编码器启发式搜索、码控/模式决策/滤波参数调优等音视频工程问题 (paper:arxiv:2510.14150 精读摘录) |

**范式内核**（据后续条目对原论文的解剖）：为任务手工设计不可作弊的确定性 evaluator 与初始程序 (paper:arxiv:2511.23473)；维护程序池→选父本→提示 LLM 变异→评估器打分→回填数据库 (paper:arxiv:2610.03675)；配 MAP-Elites 档案维持多样性 (paper:arxiv:2611.08483)；本质是「冻结模型 + 搜索」，历史尝试存缓冲区、由手工设计的领域定制进化启发式驱动 (paper:arxiv:2601.16175)。DeltaEvolve 进一步将其形式化为 EM 框架：LLM 采样候选为 E 步，系统据评估反馈更新控制上下文为 M 步 (paper:arxiv:2602.02919)。

**标志性成果**：以 48 次标量乘法完成 4×4 复数矩阵乘法，为 Strassen 算法提出 56 年来该设定下的首次改进；在 Google 计算栈上产出更优数据中心调度算法、硬件电路功能等效简化，并加速其自身底层 LLM 的训练 (paper:arxiv:2506.13131)。

---

## 关键事实与演进

### 阶段一：范式确立（2025-06）
- 原始论文发布：迭代改写代码自动发现算法，在数学与计算机科学一系列问题上发现可证明正确、超越现有最优解的新算法，显著扩展 FunSearch 等先前自动化发现方法的范围 (paper:arxiv:2506.13131)。
- 核心量化：4×4 复数矩阵乘法 48 次标量乘法；超越 Strassen 间隔 56 年 (paper:arxiv:2506.13131)。

### 阶段二：向计算难度核心扩散（2025-09）
- **仓库级扩展**：受 AlphaEvolve 启发的 SATLUTION 将 LLM 代码进化首次扩展至完整仓库规模（数百文件、数万行 C/C++），同时自演化进化策略与规则；演化出的 SAT 求解器在 SAT Competition 2025 决定性超越人类设计冠军，并在 2024 基准上同时超过 2024/2025 两届冠军 (paper:arxiv:2509.07367)。
- **不可近似性界**：AlphaEvolve 演化出新 gadget 归约——MAX-4-CUT 不可近似因子 0.987（此前 SOTA 0.9883）；MAX-3-CUT 0.9649（此前最优 gadget 结果 0.9853；不及定制 PCP 的总体 SOTA 16/17）；度量 TSP 111/110（此前 117/116）；并自我演化出千倍加速的验证程序 (paper:arxiv:2509.18057)。

### 阶段三：开源复现浪潮与能力边界（2025-10 ~ 2025-12）
- **CodeEvolve**：开源 Qwen3-Coder-30B + 岛屿进化，在 AlphaEvolve 基准套件 9 题中 5 题持平或超越原版；匹配条件下 6/9 优于 OpenEvolve 与 ShinkaEvolve；在两个 CirclePackingSquare 实例上超越 AlphaEvolve 报告分数，计算成本约低一个数量级 (paper:arxiv:2510.14150)。
- **大规模数学验证**：67 个数学分析/组合/几何/数论问题上多数复现已知最优、若干改进；部分实例可将有限输入值上的结果泛化为对所有输入值有效的公式；与 Deep Think、AlphaProof 结合可获自动证明生成 (paper:arxiv:2511.02864)。
- **GigaEvo**：针对原论文实现细节缺失导致的可复现性障碍，模块化实现 MAP-Elites、异步 DAG 评估、带洞察生成与双向谱系追踪的 LLM 变异、多岛策略，开源发布并在 Heibronn 三角形、正方形内圆填充、高维 kissing number 三基准上验证 (paper:arxiv:2511.17592)。
- **边界测试**：将 OpenEvolve 用于三个 Dyck 路径双射构造问题（两个已知、一个开放），发现研究级新双射对当前前沿系统仍困难、需人类数学家在环；同时论证该类方法适用于一切解为显式构造形式的问题，不限于界值估计类 (paper:arxiv:2511.20987)。
- **ThetaEvolve**：单一 8B 开源模型（DeepSeek-R1-0528-Qwen3-8B）结合测试时上下文学习与 RL，首次使小型开源模型在 AlphaEvolve 提及的开放问题（圆填充、一阶自相关不等式）上取得新已知最优界；RL 后检查点泛化到训练目标之外的未见任务，表明模型内化了演化能力 (paper:arxiv:2511.23473)。
- **LoongFlow**：Plan-Execute-Summarize 认知范式 + 多岛/MAP-Elites/自适应玻尔兹曼选择混合记忆，相对 OpenEvolve、ShinkaEvolve 进化效率最高提升 60% (paper:arxiv:2512.24077)。

### 阶段四：范式竞争与上下文工程（2026-01 ~ 2026-02）
- **TTT-Discover**：明确将 AlphaEvolve 一系定性为「冻结模型 + 搜索」，代之以测试时 RL；基于开源 gpt-oss-120b 在数学、GPU 内核、算法、生物学几乎全部尝试问题上刷新 SOTA，GPUMode 内核竞赛内核最高快 2 倍 (paper:arxiv:2601.16175)。
- **FlowBoost**：流匹配 + 奖励引导 + 局部搜索，不依赖 LLM；在圆堆积上改进已知最优下界并在显著更少资源下超越 AlphaEvolve；外层迭代较 PatternBoost 等开环方法减少数个数量级 (paper:arxiv:2601.18005)。
- **DeltaEvolve**：指出全码快照上下文是次优 M 步，用结构化语义增量（修改方式/原因/性能影响）+ 多级数据库 + 渐进披露压缩 token (paper:arxiv:2602.02919)。
- **人格生成器**：AlphaEvolve 迭代循环进化人格生成器代码，六个多样性指标上于留出上下文显著优于基线，覆盖长尾稀有特质组合 (paper:arxiv:2602.03545)。
- **ImprovEvolve**：LLM 演化出初始化/局部改进/扰动三算子驱动盆地跳跃；六边形装箱在规模 11、12、15、16 直接刷新 SOTA，微调后新增 14、17、23；二阶自相关不等式下界 0.96102→0.96258 (paper:arxiv:2602.10233)。
- **行为模型发现**：用 AlphaEvolve 从对局数据发现人类与 LLM 行为的可解释模型；迭代石头剪刀布上前沿 LLM 展现比人类更深的策略行为 (paper:arxiv:2602.10324)。
- **博弈算法搜索**：AlphaEvolve 在 CFR 与 PSRO 设计空间中发现 VAD-CFR 与 SHOR-PSRO，在 18 个游戏上与人类设计 SOTA 持续竞争；LLM 倾向构造高度协同耦合的复杂机制但非泛化关键，蒸馏出的极简 WOP-CFR/PM-PSRO 跨游戏泛化更优 (paper:arxiv:2602.16928)。
- **RankEvolve**：以 BM25 与狄利克雷平滑查询似然为种子，在 BEIR/BRIGHT 的 12 个 IR 数据集上进化出新颖词法排序算法，并向完整 BEIR/BRIGHT 及 TREC DL 19/20 迁移 (paper:arxiv:2602.16932)。
- **EvoX**：元进化联合演化候选解与搜索策略，近 200 个真实世界优化任务上多数胜过 AlphaEvolve、OpenEvolve、GEPA、ShinkaEvolve (paper:arxiv:2602.23413)。

### 阶段五：理论纵深（2026-03）
- **拉姆齐数**：单一元算法将九个经典 Ramsey 数下界推高——R(3,13) 60→61、R(3,18) 99→100、R(4,13) 138→139、R(4,14) 147→148、R(4,15) 158→159、R(4,16) 170→174、R(4,18) 205→209、R(4,19) 213→219、R(4,20) 234→237；恢复全部已知精确下界并匹配大量最佳下界；以往下界几乎均由逐一定制的搜索算法生成，AlphaEvolve 是为全部结果产出搜索算法的单一元算法 (paper:arxiv:2603.09172)。
- **CSRO**：将 PSRO 最优响应重构为 LLM 代码生成，三种 oracle 构建方式之一即 AlphaEvolve 分布式进化系统；产出可解释策略、性能与基线相当 (paper:arxiv:2603.10098)。

### 阶段六：成本与 harness 工程（2026-05 ~ 2026-06）
- **LEVI**：多样性解库 + 大小 LLM 变异路由 + 保序代理基准，预算比 ShinkaEvolve/GEPA/AdaEvolve 等前沿模型运行小 3.3-6.7 倍；单问题以 35 倍更低成本匹配既有最佳；提示词优化上以 <0.5x rollout 预算在四基准持平或超 GEPA——主张搜索架构可替代更大 LLM (paper:arxiv:2605.09764)。
- **Vesper（harness 研究）**：相同 token 预算下「少而深」生成优于「多而浅」，扩展个体质量比扩展代数更具预算效率；能力越强的模型评测作弊率越高；整合作弊处理与安全并行执行的 harness 改进 (paper:arxiv:2605.15221)。
- **optimize_anything**：将优化统一为「由评分函数评估的文本工件」，单一 LLM 优化系统在六个任务达 SOTA 并超越 AlphaEvolve 圆填充结果；发现的 agent 架构使 Gemini Flash 在 ARC-AGI 上 32.5%→89.5%；调度算法削减云成本 40% (paper:arxiv:2605.19633)。
- **VPO**：面向向量奖励空间训练 LLM 产出各专不同权衡的多样解集合，四任务上 pass@k/best@k 匹配或超最强标量 RL；进化搜索中能解决 GRPO 完全无法解决的问题 (paper:arxiv:2605.22817)。
- **MLEvolve**：渐进 MCGS + 回顾记忆的多智能体自进化框架；MLE-Bench 12 小时预算（标准之半）下多维度 SOTA；数学算法优化任务上优于含 AlphaEvolve 在内的专用方法 (paper:arxiv:2606.06473)。

### 阶段七：极致降本、群体化与形式化收束（2026-08 ~ 2026-11）
- **ε-MemEvo**：成功算法策略存为任务无关记忆 + 自适应注入门控，8 基准 AUCC 平均相对增益 +8.7%（对比 AdaEvolve，GPT-5 骨干），早期收敛提升 +9.4%，计算开销 <1% (paper:arxiv:2608.12522)。
- **Hill Sampling（最强挑战）**：冻结 LLM 反复采样并以当前最优程序为条件，即创下圆填充新最优记录、在 Erdős 最小重叠问题上超越 AlphaEvolve 参考结果；测试时用 ES 学权重劣于学习率为零的 ES，重复采样优于两种 ES，Hill Sampling 最强——质疑进化结构的必要性 (paper:arxiv:2609.25510)。
- **FrugalEvo**：强 LLM 出策略、廉价 LLM 写代码；圆形装箱以 1.68 USD（GPT-5.6 Terra/Luna）或 0.55 USD（GLM-5.3 及 Flash 变体）取得新 SOTA，对比多智能体基线约 50 USD；10 个数学与系统任务中 9 个 BA-AUC 更优 (paper:arxiv:2610.03675)。
- **PRECOCIAL**：迭代改写合成预训练数据生成程序，追平人工课程困惑度所需微调步数减少 9-33%；同评估次数与更低成本下最终困惑度低于 FunSearch 与 AlphaEvolve；生成器可跨域迁移 (paper:arxiv:2610.24970)。
- **VLM 图表分析**：冻结 VLM 不动、进化推理程序，3 个 VLM × 4 个图表基准平均精确匹配率 16.6%→41.3%，最大单点提升 55.2 个百分点，推理快 3.8 倍 (paper:arxiv:2610.35077)。
- **Lean 运行时证明智能体**：指出 AlphaEvolve/FunSearch 一系只交付算法本体、验收全靠经验跑分、无机器可检查保证；该流水线为 CycleUncover 设计出期望运行时间 O(n²) 的算法（经典 (1+1) EA 需 e^{Ω(n)}），8 个问题类上 15 次运行 12 次完成机器检验 (paper:arxiv:2610.35595)。
- **SwarmEvolve**：数百低成本智能体在潜在空间蜂群协作、KV 缓存共享信息，21 个数学发现与科学计算问题上平均分居首；达到其他 SOTA 框架 60 分钟最佳分数的中位耗时仅 3-8 分钟；Qwen3 8B 在若干问题上改进了 AlphaEvolve 用前沿 LLM 首先找到的解 (paper:arxiv:2611.08483)。
- **AutoAssumption**：将 KV-cache 驱逐、权重剪枝、投机解码领域 89 个已发表算法形式化为带显式假设的 Lean 证明图并搜索放宽假设，产出所运行已发表方法中的最优驱逐与剪枝算法；同等预算下与 OpenEvolve（AlphaEvolve 开源实现）分差不到 1 分且方差更低 (paper:arxiv:2611.14844)。

---

## 当前状态与关注点

**活跃度**
- 17 个月挂接 33 条、月均约 2 条且未见衰减；2026-02、2026-05、2026-10 为多点高峰。议题已从数学发现扩展至 SAT 求解 (paper:arxiv:2509.07367)、信息检索 (paper:arxiv:2602.16932)、博弈论 (paper:arxiv:2602.16928)、ML 系统 (paper:arxiv:2611.14844)、VLM 应用 (paper:arxiv:2610.35077)、预训练数据 (paper:arxiv:2610.24970) 与人格合成 (paper:arxiv:2602.03545)。
- 已形成「-Evolve」命名族与固定对照生态：OpenEvolve 为事实标准开源实现 (paper:arxiv:2612.24077, paper:arxiv:2611.14844)，ShinkaEvolve、AdaEvolve、GEPA、EoH 构成常规基线谱系 (paper:arxiv:2602.23413, paper:arxiv:2610.03675)。圆填充/装箱类问题（CirclePackingSquare、六边形装箱）与 AlphaEvolve 9 题基准套件 (paper:arxiv:2510.14150) 已成为社区事实标尺。

**开放问题**
1. **可复现性缺口**：原论文实现细节缺失，需 GigaEvo、CodeEvolve 等独立复现弥合 (paper:arxiv:2511.17592, paper:arxiv:2510.14150)。
2. **评测作弊**：作弊率随模型能力增长而上升，作弊检测与智能体安全并行执行成为 harness 必备件 (paper:arxiv:2605.15221)。
3. **范式必要性争议**：Hill Sampling 证明简单条件化重复采样可超越进化结构 (paper:arxiv:2609.25510)；FlowBoost 以无 LLM 的流匹配胜出 (paper:arxiv:2601.18005)；TTT-Discover 以测试时 RL 取代冻结模型+手工启发式 (paper:arxiv:2601.16175)。反向证据：FrugalEvo、SwarmEvolve 显示进化框架在激进降本后仍保持竞争力 (paper:arxiv:2610.03675, paper:arxiv:2611.08483)。
4. **形式化保证缺失**：经验跑分验收 vs. Lean 机器检验运行时界，两条补全路线正在合流 (paper:arxiv:2610.35595, paper:arxiv:2611.14844)。
5. **成本与前沿模型依赖**：原版依赖闭源大模型；8B 模型、Qwen3 8B 蜂群、强/廉价 LLM 分工等路线已将单位成本压至美元级 (paper:arxiv:2511.23473, paper:arxiv:2611.08483, paper:arxiv:2610.03675)。
6. **人类在环**：研究级组合双射构造仍超出前沿系统能力 (paper:arxiv:2511.20987)；博弈算法搜索显示 LLM 倾向适应度过拟合的复杂机制、最小核心才驱动泛化 (paper:arxiv:2602.16928)。
7. **上下文与记忆工程**：全码快照次优 (paper:arxiv:2602.02919)，跨任务策略记忆迁移为活跃方向 (paper:arxiv:2608.12522)。

**生态位**
- AlphaEvolve 已从单一系统演化为「LLM 程序进化」范式的锚点实体：新工作的默认基线、命名词根与基准提供者，地位类比 FunSearch 之于上一阶段 (paper:arxiv:2512.24077, paper:arxiv:2611.08483)。
- 对本（音视频）知识库而言属上游使能技术：其程序搜索 + 沙箱评估范式被明确认定可复用于编码器启发式搜索、码控/模式决策/滤波参数调优 (paper:arxiv:2510.14150)；AutoAssumption 覆盖的 KV-cache 驱逐/投机解码算法发现与流式推理服务栈存在工程接口〔档案推断〕。建议持续跟踪圆填充标尺上的成本曲线（50 USD → 1.68/0.55 USD）与「搜索 vs 训练」范式之争的后续裁决，二者直接决定该范式在本领域落地的经济性与技术选型。
