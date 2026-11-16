# QP · 实体档案

> concept:QP · 数据截止 2026-11-16 · 关联 42 条 · glm-5.3

# 实体档案：Quantization Parameter（concept:QP）

## 档案概览

| 项 | 内容 |
|---|---|
| 实体 | concept:QP｜Quantization Parameter｜别名：量化参数、quantization parameter |
| 定义定位 | 混合块编码框架中控制变换系数量化强度的参数：量化引入模糊与振铃失真，QP 越大越显著；VVC 中 QP 取值 1–63 (paper:arxiv:2105.05658) |
| 档案覆盖 | 42 条挂接条目，时间跨度 2016-10 至 2026-11：论文 17 篇、版本发布 17 项（Kvazaar 5、SVT-AV1 7、VVenC 4、libavif 1）、JVET 提案 8 份 |
| 四条主线 | ① RD 操作点选择器（固定 QP 编码 + BD 比较支撑点）；② 码率控制/自适应量化控制旋钮（delta-QP、QP offset、QPA、VAQ、AQ）；③ 神经网络条件信号（QP 图输入、QP 调制层、跨 QP 单模型）；④ 跨模态量化控制（点云量化参数选择） |
| 边缘条目 | libavif v1.4.0、SVT-AV1 v3.1.0/v4.1.0/v4.3.0 挂接但未含 QP 特定事实，仅作生态背景保留 |

## 关键事实与演进

### 阶段一：编码器侧 QP 控制面构建（2016–2020，Kvazaar 主线）

- **2016-10｜v1.0.0**：BD-rate 评测以 QP 17/22/27/32 为支撑点，相比 v0.8.3 全序列 3-fr 档 BD-rate -31.0%、2-vf 档 -27.1%——确立 QP 四点扫描作为编码器版本间比较的默认口径 (repo_release:github:kvazaar-v1.0.0)
- **2017-02｜v1.1.0**：码率控制下沉至 LCU 级；新增 `--roi` 实现 **LCU 级 delta-QP** 控制，即空间自适应量化的最早工程化入口之一 (repo_release:github:kvazaar-v1.1.0)
- **2017-11｜v1.2.0**：新增 360°（全景）自适应 QP (repo_release:github:kvazaar-v1.2.0)
- **2019-07｜v1.3.0**：`--set-qp-in-cu` 将 **QP 信令下移到 CU 级**，控制/信令粒度进一步细化 (repo_release:github:kvazaar-v1.3.0)
- **2020-04｜v2.0.0**：GOP 定义重构为 **QP offset 模型**（新增 16 帧层级 GOP `--gop=16`，PU 深度按 GOP 层配置）；同时引入 oba 码控与方差自适应量化 `--vaq` (repo_release:github:kvazaar-v2.0.0)

〔档案推断〕此阶段呈现明确的粒度演进轨迹：帧级固定 QP → LCU 级 delta-QP → CU 级信令 → GOP 层级 QP offset 建模。

### 阶段二：QP 作为实验条件与基准变量（2021–2023）

- **2021-04｜NTIRE 2021**：Track 1/2 明确针对 **HEVC 固定 QP** 压缩视频的质量增强（482 队注册；测试阶段三赛道分别 12/8/11 队提交）；Track 3 转向 x265 固定码率 (paper:arxiv:2104.10781)
- **2021-05｜CNN 质量增强两连发**：以规范预测信号 + 重建信号 + **QP 图**为输入的预测感知 CNN，较无预测信息版本额外 -1.3% BD-BR，帧/块级模型选择再叠加 -0.5%（VTM-10.0 RA）(paper:arxiv:2105.03338)；同月工作确立“**全部 QP 共用单一模型并以 QP-map 适配**、亮度色度共享”的降内存范式，较默认 CNN QE 滤波器同复杂度下 +1.52% BD-BR (paper:arxiv:2105.05658)
- **2022-04｜NTIRE 2022**：Track 1 延续固定 QP HEVC 质量增强赛道，发布 LDV 2.0（335 段 = 原 240 + 新增 95）(paper:arxiv:2204.09314)
- **2023-04｜BD 度量方法论警示**：BD 插值误差在 PSNR 标准应用中平均 <0.5pp，但在 VMAF/能耗/跨编解码器场景可达 5pp；**增加 QP 支撑点数量可使误差约减半**，两个支撑点仅够粗略估计 (paper:arxiv:2304.12852)——直接约束了 QP 扫描密度的实验设计规范
- **2023-08｜QP 门限效应**：4K 下采样编码 + ML 超分链路，QP>34 时平均 12%、QP>42 时平均 18% BD-rate 优于 VVC 参考软件 (paper:arxiv:2308.06570)

### 阶段三：实时通信中的多维 QP 调控（2023）

- **2023-08｜Mamba**：多智能体强化学习将 QP 与分辨率、帧率联合调控，解决 WebRTC 中网络码率决策与编码器码控不协调问题，并以课程学习提升训练效率 (paper:arxiv:2308.03643)——QP 从编码器内部参数扩展为通信系统的多维权衡维度之一。

### 阶段四：标准化中 QP 相关工具的校正与交叉验证（2023–2024，JVET/ECM）

| 时间 | 提案 | QP 相关内容 | 交叉验证 |
|---|---|---|---|
| 2023-01 | JVET-AC0123 (Canon) | ECM 中 **B 类序列 QP22 条件**下 MTT 最大深度校正——QP 作为工具参数化的分档条件 | AC0235 交叉检查 (standard_proposal:jvet:m193-AC0123, standard_proposal:jvet:m193-AC0235) |
| 2023-10 | JVET-AF0089 (AhG10) | VVC **CTU 级拉格朗日乘子与 QP 自适应** | — (standard_proposal:jvet:m196-AF0089) |
| 2024-01 | JVET-AG0055 (AhG10) | VVC **低时延配置**下 CTU 级 λ–QP 联合适配 | AG0280 交叉校验 (standard_proposal:jvet:m197-AG0055, standard_proposal:jvet:m197-AG0280) |
| 2024-04 | JVET-AH0117（字节跳动/阿里巴巴/高通/InterDigital） | ECM **色度 QP 映射表**修改 | AH0317、AH0351 两份独立交叉验证 (standard_proposal:jvet:m198-AH0117, standard_proposal:jvet:m198-AH0317, standard_proposal:jvet:m198-AH0351) |

该集群表明：λ–QP 联合适应与色度 QP 映射仍是 VVC/ECM 标准化的活跃修订对象，且工具采纳前交叉验证已成常规流程。

### 阶段五：VVenC 的 QP 级联与恒定质量模式（2024）

- **v1.12.0**：新增 **CQF 封顶恒定质量模式**——固定 QP + 启用 QPA + 最大码率约束三条件同时生效 (repo_release:github:vvenc-v1.12.0-rc2, repo_release:github:vvenc-v1.12.0)
- **v1.13.0**：新增 **GOP 自适应 QP 级联**（仅限非 QPA 场景）(repo_release:github:vvenc-v1.13.0-rc1, repo_release:github:vvenc-v1.13.0)

### 阶段六：QP 与学习方法的双向渗透（2024–2026）

- **2024-02｜DCVC-FM**：以可学习量化缩放器调制潜特征 + 训练时**均匀量化参数采样**，单模型 PSNR 质量范围由先前约 3.8 dB 扩至约 11.4 dB；单帧内设置省 29.7% 码率、MACs -16%（vs 先前 SOTA NVC）(paper:arxiv:2402.17414)——神经编解码器以连续质量缩放对齐传统 QP 梯度
- **2025-04｜快速块划分**：划分图网络内嵌 **QP 调制层**（配合堆叠自顶向下/自底向上处理与划分自适应对齐），RA 配置平均省 51.30% 编码时间、BDBR 仅 +2.12% (paper:arxiv:2504.18398)
- **2025-05｜LPCM**：球坐标量化区别于笛卡尔量化，提出基于差分进化的**量化参数选择**方法，不增编码时间改善点云率失真 (paper:arxiv:2505.20059)——QP 概念外延至点云几何压缩
- **2025-11｜主观质量基准**：以 9 个 QP × 4 分辨率（360p–2160p）× 6 源视频生成 216 条 4K 序列、30 名受试者受控评分；VMAF 与 AVQBits|H0|f 主观 Pearson 相关最强，PSNR 在序列内跨编解码器比较中 Spearman 最高 (paper:arxiv:2511.00969)
- **2026-02｜帧级比特预测**：VCA 特征 + QP 输入随机森林预测帧级比特（VVenC 编码 UHD 序列，I/P/B 帧 R² 分别 0.93/0.88/0.77），嵌入码控回路后效率与两遍码控相当、总编码时间 -33.3%——**解析式 R–QP 模型的数据驱动替代** (paper:arxiv:2602.06242)
- **2026-06｜LLM 驱动 QP 启发式**：DeepSeek 闭环进化（种群 K=4、10 轮、双提示）自动发现的帧级 QP 启发式等价于“熵约束 RDO”（score = weighted_PSNR/(1+H_QP)/log(1+total_bits)）；相对 VVenC-1.7.0 faster 固定 QP（RA、YUV-PSNR）：CTC B 类 -1.73%、UVG -1.00%、MCL-JCV -1.06%，三库总均约 -1.26% (paper:arxiv:2606.20847)
- **2026-07｜可微代理 AQ**：构建对 QP 可微的 H.264 帧内编码代理（覆盖 global-QP 与 spatial-QP 两种设置），冻结代理驱动的自适应量化相对固定 QP 基线：语义分割 BD-rate 最高 -17.12%、MS-SSIM 最高 -15.30% (paper:arxiv:2607.10478)——打通 QP 的梯度优化通道
- **2026-08｜码率分配迁移**：神经压缩模型学到的感知重要性生成 **QP 图**指导块级码率分配（不改解码语法），MS-SSIM 码率节省：vs JM-19.0 20.20%、vs HM-16.20 8.25%、vs VTM-23.0 8.37%（HEVC B~D）(paper:arxiv:2608.07799)；同月 MDFI 发布含**多 QP 级别**重建序列与 VVC 预测帧的数据集 (paper:arxiv:2608.21495)
- **2026-09｜CASR**：针对“激进量化与块划分产生的伪影”，LoRA 逐序列过拟合超分后滤波相对 VTM21：RA 配置 Y -10.93%/U -15.39%/V -24.41%，全帧内 Y -13.43%/U -5.75%/V -22.94%（JVET CTC A1/A2）(paper:arxiv:2609.37328)

### 阶段七：SVT-AV1 的 QP 参数面维护（2026）

- **v3.0.2**：补充 `--luminance-qp-bias`（亮度 QP 偏置）缺失文档 (repo_release:github:SVT-AV1-v3.0.2)
- **v3.1.1**：修复 min-qp 与 max-qp 范围检查及错误提示 (repo_release:github:SVT-AV1-v3.1.1)
- **v4.0.0**：破坏性 API 更新中 CRF 范围扩展至 70 并新增**四分之一粒度步进** (repo_release:github:SVT-AV1-v4.0.0)
- **v4.2.0**：RTC CBR 码控采用**卡尔曼滤波 QP 估计**，配合循环刷新与帧重编码 (repo_release:github:SVT-AV1-v4.2.0)

## 当前状态与关注点

### 活跃度
- 挂接密度峰值出现在 2024–2026：JVET QP 工具提案与交叉验证（2023–2024）、VVenC QPA/CQF/QP 级联（2024）、学习型 QP 控制论文（2025–2026 共 7 篇）、SVT-AV1 QP 参数面更新（2026 集中 4 项）——QP 仍是编码器迭代与学术研究的高频触点，且从“参数配置”演进为“被优化对象”。

### 技术趋势
1. **粒度持续细化**：帧级固定 QP → LCU/CU 级 delta-QP 与信令 → CTU 级 λ–QP 联合适应 → 块级神经 QP 图 (repo_release:github:kvazaar-v1.1.0; standard_proposal:jvet:m197-AG0055; paper:arxiv:2608.07799)
2. **QP 成为神经网络的标准条件信号**：QP 图输入、QP 调制层、跨 QP 单模型已成质量增强与快速算法的共同设计模式 (paper:arxiv:2105.05658; paper:arxiv:2504.18398)
3. **决策自动化与可微化**：LLM 自动进化 QP 启发式 (paper:arxiv:2606.20847)、对 QP 可微的编码器代理 (paper:arxiv:2607.10478) 分别从符号搜索与梯度两条路径接管 QP 决策
4. **解析模型让位于数据驱动**：R–QP 解析模型被 VCA 特征随机森林替代 (paper:arxiv:2602.06242)
5. **概念跨域扩散**：点云量化参数选择 (paper:arxiv:2505.20059)、神经压缩可学习量化缩放 (paper:arxiv:2402.17414)、WebRTC 多维 ABR 中的 QP 维度 (paper:arxiv:2308.03643)

### 开放问题
- **帧级 λ–QP 估计困难**：直接套用拉格朗日 RDO 于帧级 QP 因 λ 难以准确估计（λ–QP 关系、传播失真），实际可比固定 QP 更差 (paper:arxiv:2606.20847)
- **色度 QP 映射未定**：ECM 色度 QP 映射表修改仍处提案 + 两轮交叉验证阶段 (standard_proposal:jvet:m198-AH0117 系)
- **感知度量与块级 RDO 的结构性矛盾**：感知度量缺乏 MSE 的可加性与块独立性，感知导向的 QP 图分配是活跃替代路线 (paper:arxiv:2608.07799)
- **QP 扫描密度与 BD 可信度权衡**：低支撑点数下 BD 误差在非标准场景可达 5pp，BD 值低于误差阈值时不应下结论 (paper:arxiv:2304.12852)
- **量化失真的端侧补救**：大 QP 下模糊/振铃由环路滤波与后处理（含 SR 型后滤波）竞争性缓解 (paper:arxiv:2105.05658; paper:arxiv:2609.37328)

### 生态位
QP 是连接量化、率失真优化与码率控制三大机制的枢纽变量，档案内横跨 H.264/HEVC/VVC/AV1 标准实现、JVET/ECM 标准化进程、神经视频压缩、点云压缩与实时通信场景。〔档案推断〕随着神经编解码器以连续质量缩放对标 QP 梯度 (paper:arxiv:2402.17414)、LLM 与可微方法接管 QP 决策 (paper:arxiv:2606.20847; paper:arxiv:2607.10478)，QP 的角色正从“人工设定的编码参数”迁移为“被学习与被优化的决策变量”，其在传统编码器中的工程面（QPA、CQF、QP 级联、QP 估计器）则继续作为部署侧的稳定演进层。
