# BD-Rate · 实体档案

> metric:BD-Rate · 数据截止 2026-11-16 · 关联 76 条 · glm-5.3

# 滚动档案：BD-Rate

## 档案概览

| 属性 | 内容 |
|---|---|
| 实体 ID | `metric:BD-Rate` |
| 类型 | metric |
| 名称 | Bjontegaard Delta Rate |
| 定义 | 同质量下的码率变化；**负值 = 省码率**，方向为**越低越好**（注册表 notes） |
| 强制口径约束 | 必须带锚点与失真测度（如 vs 固定QP / YUV-PSNR、vs x265 veryslow / MS-SSIM）；**无锚点的 BD-Rate 不可比**（注册表 notes） |
| 挂接条目 | 76 条：论文 69、标准提案 4（均为 JVET）、版本发布 3（均为 SVT-AV1） |
| 时间跨度 | 2021-12 至 2026-11，约 5 年；2026 年条目密度显著最高〔档案推断：与神经压缩（LIC/NVC/INR/扩散/3DGS）研究产出扩张及本库采集范围扩大相关〕 |
| 覆盖域 | 传统视频编码、神经图像/视频压缩、点云（G-PCC/V-PCC）、体积视频（NeRF/3DGS）、语音、VCM/ICM 机器视觉、流媒体码率阶梯、编码器加速与码控 |

该实体的本质特征：它不是被评测的对象，而是**全部压缩研究的通用计分货币**——76 条挂接中每一条都把 BD-Rate 作为验收指标使用，覆盖锚点从 HM/VTM/ECM/AVM 到 G-PCC PredLift/RAHT、x265、HLS 阶梯乃至扩散式 SOTA 基线。

---

## 关键事实与演进

### 2021–2022：点云域早期应用与标准化机构的指标治理

- 点云压缩率先大量挂接：MS-GAT 对 G-PCC 属性伪影去除，vs Predlift 平均 −9.74%、vs RAHT 平均 −10.13%（多种点云测试平均）[paper:arxiv:2112.00560]；OctAttention 无损几何编码 vs 此前 SOTA 增益 10%–35%（SemanticKITTI/MPEG 8i/MVUB）[paper:arxiv:2202.06028]；D-DPCC inter 模式 vs V-PCC v13 平均省 76% [paper:arxiv:2205.01135]；帧间几何压缩 vs G-PCCv20 Octree >88%、vs Trisoup >56%、vs V-PCC intra >62% [paper:arxiv:2207.12554]——注意这些大数值均限定"inter 模式/特定属性/有损几何"口径。
- **BD-Rate 反向驱动标准设计**：JVET 在 ECM 平台上连续处理亮度/色度 BD-rate 分量失衡问题——调整编码配置以平衡 luma/chroma 增益 [standard_proposal:jvet:m189-Y0113] → 组合 Y0102+Y0113 测试 [standard_proposal:jvet:m189-Y0223] → 交叉检验 [standard_proposal:jvet:m189-Y0227]，2023 年延续为 AC0138 [standard_proposal:jvet:m193-AC0138]。这是指标分量结构（Y/Cb/Cr）直接参与工具取舍的档案证据。

### 2023：学习式图像压缩起势、NNVC 标准口径与复杂度-RD 交易

- LIC 对 VTM 锚点的增益序列形成：LLIC vs VTM-17.0 Intra −9.49%/−9.47%/−10.94%（Kodak，熵模型对齐）[paper:arxiv:2304.09571]；ConvNeXt-ChARM vs VTM-18.0 PSNR 口径 −5.24% [paper:arxiv:2307.06342]；MLIC++ vs VTM-17.0（Kodak, PSNR）−13.39% [paper:arxiv:2307.15421]；FAT vs VTM-12.1 −14.5%（Kodak）/−15.1%（Tecnick）[paper:arxiv:2310.16387]。锚点版本与数据集已开始碎片化。
- NNVC 标准化以 BD-Rate 定案：NNVC-4.0 的 NN 工具 vs VTM-11.0_nnvc，RA 配置 Y/Cb/Cr −11.94%/−21.86%/−22.59%，低延迟 −9.18%/−19.76%/−20.92% [paper:arxiv:2309.05846]。
- **BD-Rate 作为复杂度定价单位**确立：VVC 两遍码控低复杂度替代以 +2% 平均 BD-rate 买 32% 编码时间 [paper:arxiv:2306.16786]；帧间划分加速以 +0.37%–1.18% 买 17%–30% 提速 [paper:arxiv:2312.10567]。同条目还固化了行业基准事实：VVC vs HEVC 约 50% BD-rate 增益（JVET 2020 定稿口径），代价是编码复杂度约 10×。
- 口径向机器视觉扩展：VCM 特征压缩 vs 先前方法 ≥52%（目标检测任务）[paper:arxiv:2306.16670]；跨平台实时神经编解码出现（720P/25FPS，vs H.265 最多省 24.2% 码率）[paper:arxiv:2309.11276]——跨平台位失配问题首次进入档案，将成为后续 BD-Rate 可信度议题的前奏。

### 2024：小增益工具时代、编码器阵营横评与体积视频

- 标准内增量工具的典型量级为 <2%：SAIP vs VTM 12.0 LDP 平均 −0.82%/最高 −1.98% [paper:arxiv:2403.11694]；LUT 环路滤波 vs VTM-11.0 AI −0.13%/−0.34%/−0.51% [paper:arxiv:2407.10926]；UAMM LDP 平均 −0.13%/最高 −0.38% [paper:arxiv:2407.11541]。
- **阵营横评确立生态位排序**：低时延配置下 ECM 综合最优，vs AOM AVM 省 16.1%、vs DCVC-FM 省 11.0%（PSNR，MPEG/AOM CTC 序列，YCbCr 4:2:0）[paper:arxiv:2408.05042]；同文记录 DCVC 系在大背景运动内容上表现不稳定——神经编码器的 BD-Rate 一致性成为开放问题。
- 感知/任务口径扩散：CLIC vs VVC MSE 约 −10%、MS-SSIM >50% [paper:arxiv:2401.11615]；SCH vs VTM-23.1 四数据集 −18.54%/−23.98%/−22.33%/−24.71% [paper:arxiv:2409.14090]；NeRF 体积视频 vs TeTriRF：HumanRF 约 −80%、ReRF 约 −60% [paper:arxiv:2411.05322]。
- 跨平台量化代价被量化：SSF+静态量化同机 BD-rate 平均 +9.93%（UVG）/+9.02%（HEVC-B）[paper:arxiv:2410.20145]——部署鲁棒性以显式 BD-Rate 税形式入档。

### 2025：标准化节点与感知口径全面铺开

- **JPEG AI 以七感知指标 BD-rate 均值口径**报出 vs VVC intra：主档（低复杂度）13.1%、高档 19.2% [paper:arxiv:2503.16288]；标准综述确认 MS-SSIM/FSIM/VIF/VMAF/PSNR-HVS/IW-SSIM/NLPD 多指标 BD-rate 显著降低 [paper:arxiv:2510.13867]。
- INR 视频里程碑：GIViC 成为首 个 RA 配置下超越 VTM 的 INR 编码器（−15.94% vs VTM、−22.46% vs DCVC-FM、−8.52% vs NVRC，YUV 4:2:0 GOP32）[paper:arxiv:2503.19604]。
- 扩散/生成式压缩带来超大感知口径数字：ResULIC vs SOTA 扩散基线 LPIPS −80.7%、FID −66.3% [paper:arxiv:2505.08281]；GFix vs GSVC LPIPS 最多 −72.1%、FID 最多 −21.4% [paper:arxiv:2511.06953]。
- 点云属性增强继续：PCE-GAN vs PredLift −19.2%/vs RAHT −18.3%（平均）[paper:arxiv:2503.00047]；推理期内容自适应使 DCVC-FM 在个别大运动视频上 up to 41% [paper:arxiv:2510.07283]——"up to"口径占比上升。
- 复杂度归一化变体口径出现：ShiftLIC 报每像素 MACs 归一化 BD-rate 增益 −102.6%（vs VVC Intra/GMM 等对比集）[paper:arxiv:2503.23052]，属非标准口径，横比需谨慎。

### 2025 末–2026：全域渗透、部署可信度与工业发布口径

- **扩展至语音域**：ECC vs 传统与神经编解码基线平均 −39.9%（ViSQOL）/−76.3%（PESQ）[paper:arxiv:2606.11631]。
- 3DGS 体积视频量级跃升：SAGA vs GIFStream −90.88%、vs TED-4DGS −64.30%（Neu3D，PSNR）[paper:arxiv:2609.33969]。
- **AV2 CTC 正式定义评估口径**：AV2 v13.0 vs AV1 基准，RA 配置 PSNR-YUV −29.81%、VMAF −33.79%，并新增凸包自适应流/UGC/扩展色度格式评估 [paper:arxiv:2605.15800]。工业侧 SVT-AV1 三个版本以模式/预设绑定的口径报数：RTC 模式约 5–10% 改善（v3.1.0）[repo_release:github:SVT-AV1-v3.1.0]、AVIF 同等复杂度约 5–8%（v4.0.0）[repo_release:github:SVT-AV1-v4.0.0]、TUNE-VMAF 目标约 15% VMAF BD-rate（v4.2.0）[repo_release:github:SVT-AV1-v4.2.0]。三条同日挂接，〔档案推断：为批量补录而非同日发布〕。
- 部署可信度成为 BD-Rate 前提条件：MLVC 指出不同厂商 NPU 浮点不可逐位复现会使熵解码崩溃、令纸面 BD-Rate 失效，其跨平台（TH XP）口径 vs HEVC-QSV 达 −58.7% [paper:arxiv:2606.28027]；V-PCC 分帧编码的跨 slice 冗余损失带来最高 5% BD-Rate 惩罚 [paper:arxiv:2606.29179]。
- 锚点谱系持续扩容：可扩展编码（S-NVRC vs SHM-12.4 −43.7%、vs 多层 VTM-20.0 −5.6%，UVG）[paper:arxiv:2609.04273]；码率阶梯（DQ-Ladder vs Apple HLS 阶梯，XPSNR ≥10.3%，VVC 工具链 750 序列）[paper:arxiv:2603.13597]；编码器代际（H.266 vs H.264 VMAF 最高 −71.3%，四数据集×四编码器评测）[paper:arxiv:2603.26763]；后处理（CASR vs VTM21 RA：Y −10.93%/U −15.39%/V −24.41%）[paper:arxiv:2609.37328]；INR 轻量档（NVRC++ S3 vs x265 veryslow −69.23%，UVG PSNR）[paper:arxiv:2606.28163]。
- 任务/感知口径进入编码内环：H.264 可微代理 AQ 在语义分割任务 BD-rate 最高 −17.12%、MS-SSIM −15.30% [paper:arxiv:2607.10478]；IDQD-RDO 在五种 FR-IQA 目标度量下节省 14.2%–36.7%（Kodak+CLIC）[paper:arxiv:2609.30077]；MoECodec 将 BD-rate 用于下游分类/检测/分割（−7.74/−8.98/−9.72，vs TransTIC 的 +35.77/+26.09/+12.83）[paper:arxiv:2606.21033]。
- 口径敏感性的反向案例：DiffCR vs SOTA 扩散基线，PSNR 口径 −65.1% 反而大于 LPIPS 口径 −27.2% [paper:arxiv:2601.10373]；InnVC vs x265 同方法 PSNR −21.66%/MS-SSIM −46.06% [paper:arxiv:2606.13957]——同一方法在不同测度下量级可差 2 倍以上。
- 国内标准进程：RDOSkip 时域跳过决策被 AVS NVC 采纳，AVS/HEVC 数据集 vs 基线 NVC 分别省 0.90%/1.29% [paper:arxiv:2611.00181]；训练配方级微增益也可入账（噪声正则化训练 −2.60% 至 −0.85% vs 复现骨干；DMCI-Large vs VTM-22.0 达 −22.02%）[paper:arxiv:2611.10073]。

---

## 当前状态与关注点

### 活跃度
高频、跨域、持续增长。挂接条目 2026 年约占全档案 40%〔档案推断：按条目年份粗计〕；使用主体从标准化机构（JVET/NNVC、JPEG AI、AOM AV2 CTC、AVS NVC）经学术评测（LIC/NVC/INR/扩散/点云/3DGS）延伸到工程发布说明（SVT-AV1）。档案内无对 BD-Rate 计算方法本身的改进或争议条目，〔档案推断：该指标方法学已趋稳定，活跃争议集中在"口径"而非"公式"〕。

### 开放问题（口径风险清单）
1. **锚点版本碎片化**：仅 VTM 锚点就并存 11.0/12.1/13.2/17.0/17.1/18.0/20.0/21/22.0/23.1 [paper:arxiv:2309.05846, 2310.16387, 2603.06766, 2510.13867, 2611.15670, 2606.21033, 2609.04273, 2609.37328, 2605.15800 等]。同为"超越 VVC"结论不可横比（如 HiDE vs VTM-12.1 报 −18.5% [paper:arxiv:2603.06766]，SCH vs VTM-23.1 报 −18.54%~−24.71% [paper:arxiv:2409.14090]）。
2. **失真测度谱系过宽**：PSNR（YUV/RGB/PSNR-HVS）、MS-SSIM、LPIPS、FID、VMAF、XPSNR、point-to-point PSNR [paper:arxiv:2308.12535]、ViSQOL/PESQ [paper:arxiv:2606.11631]、七感知指标均值 [paper:arxiv:2503.16288]、机器任务指标 [paper:arxiv:2606.21033]。感知口径数字普遍大于保真口径（ResULIC LPIPS −80.7% [paper:arxiv:2505.08281]），但存在反例（DiffCR PSNR −65.1% > LPIPS −27.2% [paper:arxiv:2601.10373]），跨测度量级不可换算。
3. **up to / 平均 / 单点混用**：MobileNVC 48%（up to，低时延）[paper:arxiv:2310.01258]、SCP 29.14%（up to）[paper:arxiv:2308.12535]、内容自适应 41%（up to，单视频、无微调）[paper:arxiv:2510.07283] 与各 JVET/CTC 平均值口径并存。
4. **部署可复现性**：跨平台位失配可使纸面 BD-Rate 在真实部署中失效 [paper:arxiv:2309.11276, 2410.20145, 2606.28027]；神经编码器在特定内容（大背景运动）上性能不稳定 [paper:arxiv:2408.05042]。
5. **非标准派生口径**：按每像素 MACs 归一化的 BD-rate（−102.6%）[paper:arxiv:2503.23052]、BD-PSNR 与 BD-Rate 双报并存（0.43 dB ↔ 14.0%，G-PCC 测试模型，稠密点云 Y 分量）[paper:arxiv:2303.13764]。

### 生态位
BD-Rate 是本知识库覆盖期内压缩领域唯一的**跨域通货**：标准组织以之为验收货币（NNVC 采纳阈值 [paper:arxiv:2309.05846]、AV2 CTC [paper:arxiv:2605.15800]、JPEG AI [paper:arxiv:2503.16288]、AVS NVC [paper:arxiv:2611.00181]）；学术端以之为 SOTA 声明货币（增益量级从标准内工具的 <2% 到跨范式替换的 >60%）；工程端以之为复杂度-性能权衡货币（加速买时间、量化保鲁棒的"税率"均已量化入档）。其治理重心已从"如何计算"转移到"锚点-测度-口径三元组如何声明"，与注册表 notes 的强制性约束完全一致：**无锚点的 BD-Rate 不可比**。
