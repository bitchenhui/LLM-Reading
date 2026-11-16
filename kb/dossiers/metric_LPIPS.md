# LPIPS · 实体档案

> metric:LPIPS · 数据截止 2026-11-16 · 关联 33 条 · glm-5.3

# LPIPS（metric:LPIPS）滚动档案

## 档案概览

| 字段 | 内容 |
|---|---|
| 注册 id | metric:LPIPS |
| 类型 | metric |
| 名称 | Learned Perceptual Image Patch Similarity |
| 方向 | 越低越好 |
| 注册表定位 | 感知距离，生成式压缩的主指标之一 |
| 挂接条目 | 33 条（全部为论文），跨度 2021-02-05 → 2026-11-03 |

**档案内角色分布（可数统计）**：
- **损失函数/优化目标**：GAN 超分训练中替代 VGG 损失（paper:arxiv:2102.03113）；
- **评测/竞赛口径**：NTIRE 2021 双赛道计分（paper:arxiv:2105.04872），以及 GLVC、YODA、ZeroGVC 等 SOTA 声明；
- **BD-rate / 匹配质量锚点**：ResULIC、GFix、DiffCR、GenVC、Gen2-VC、ENVC 等十余条；
- **研究与批判对象**：被 Wasserstein 失真正面挑战（paper:arxiv:2412.00505）、被检验对扩散 VSR 的预测力（paper:arxiv:2605.25940）、被论证不可块分解从而无法进入编码内循环（paper:arxiv:2609.30077）、被指出语义保真盲区（paper:arxiv:2606.21030）；
- **变体/无参考化**：uLPIPS（paper:arxiv:2604.19512）、代理参考估计（paper:arxiv:2607.23321）；
- **设计变量分析工具**：码本容量 vs 分辨率的对数线性回归（paper:arxiv:2607.23366）。

压缩/传输场景条目 22/33，其余为超分/修复（6）、质量评估研究（4）、世界模型（1），与注册表"生成式压缩主指标"定位吻合。本档案无 LPIPS 自身版本迭代记录；唯一观测到的结构变体为更换骨干的 TinyUSFM-uLPIPS（对标 VGG-LPIPS 基线，paper:arxiv:2604.19512）。

---

## 关键事实与演进

### 阶段一（2021）：损失函数与竞赛指标的双重登场

- **作为感知损失**：监控人脸超分工作中，将 GAN 超分常用 VGG 损失替换为 LPIPS 损失，在真实与人工退化人脸图像上均得到细节更丰富、噪声更低的重建并超越 SoTA（paper:arxiv:2102.03113）。同文指出传统无参考 IQA 无法捕捉该感知改进，NIMA 经 Mean Opinion Rank 验证相关性更好——早期即暴露"指标选型与人类感知对齐"议题。
- **作为竞赛口径**：NTIRE 2021 去模糊赛道 1（低分辨率）最佳 PSNR/SSIM/LPIPS、赛道 2（JPEG 伪影）最佳 SSIM/LPIPS（paper:arxiv:2105.04872）——LPIPS 在 2021 年已与 PSNR/SSIM 并列为挑战赛三元组。

### 阶段二（2022–2023）：档案空窗

无挂接条目。〔档案推断〕此为采集范围或入库密度问题，不能据此断言 LPIPS 社区使用停滞。

### 阶段三（2024）：生成式压缩的锚点 + 首个正面挑战者

- **低码率/极低码率的胜负判据**：扩散解码端方案码率低至 0.02 bpp，在低 bpp 区间以 LPIPS、FVD 衡量优于 H.264/H.265（paper:arxiv:2402.08934）；Promptus 以提示词流替代视频流，同等感知质量下较 H.265 带宽降低 >4×，极低码率下 LPIPS 相对 VAE 改善 0.139、相对 H.265 改善 0.118（paper:arxiv:2405.20032）。
- **扩展到 3DGS 流媒体**：LapisGS 以约 23% 原始模型体积，最高档带宽条件下 SSIM 提升 50.71%、LPIPS 提升 286.53%（相对原始 3DGS，改进幅度口径，paper:arxiv:2408.14823）。
- **首个正面挑战**：C3 以 Wasserstein 失真（WD）为优化目标，人类评分研究显示 WD 作为优化目标明显优于 LPIPS；WD 对人类评分 Elo 的预测 Pearson 相关系数 94% 以上，优于 LPIPS、DISTS 与 MS-SSIM；且解码计算量仅为 HiFiC 等生成式压缩的 <1%（paper:arxiv:2412.00505）。

### 阶段四（2025）：BD-rate 主口径的确立

- INR 视频编码以 PSNR/LPIPS 双口径报告（NVTM：UVG(Dynamic) LPIPS 改善 0.019、MCL-JCV(Dynamic) 改善 0.013，paper:arxiv:2505.00335）。
- 扩散式超低码率压缩以 LPIPS 口径 BD-rate 为主要报点（ResULIC：相对 SOTA 扩散方法 LPIPS 口径 BD-rate −80.7%、FID 口径 −66.3%，paper:arxiv:2505.08281）。
- GLVC 在多基准 DISTS 与 LPIPS 达 SOTA，用户研究显示约 1/2 码率即可匹配最新神经视频编解码器主观质量（paper:arxiv:2510.09987）。
- 3DGS 视频压缩 + 单步扩散增强路线成形（GFix：相对 GSVC LPIPS 口径 BD-rate 最多节省 72.1%、FID 口径 21.4%，paper:arxiv:2511.06953）。

### 阶段五（2026，23 条）：密集使用、系统性反思与变体衍生

**（a）一步/少步扩散压缩以 LPIPS 为主轴**：率–失真–感知（RDP）三角制约成为共同背景叙事（paper:arxiv:2601.01141 精读）。YODA 在 LPIPS/DISTS/FID/KID 四指标达 SOTA（paper:arxiv:2601.01141）；DiffCR 两步解码、LPIPS 口径 BD-rate 节省 27.2%（PSNR 口径 65.1%）、解码加速 >10×（paper:arxiv:2601.10373）；DiV-INR 在 <0.05 bpp 区间 BD-LPIPS=0.214（相对 HEVC），并在 UVG/MCL-JCV/JVET-B 上以 LPIPS/DISTS/FID 优于 VVC 及基线（paper:arxiv:2604.08329）；GenVC 匹配 LPIPS 条件下相对 GLVC 平均节省 62.5% 码率（paper:arxiv:2607.22772）；ZeroGVC 免训练方案在 JVET Class C 以 LPIPS/DISTS/FID/DOVER 领先 VVC/HEVC/DCVC-FM/DCVC-RT/GLC-Video，高分辨率高码率优势收窄（论文推测 tiling 弱化生成先验，paper:arxiv:2606.22371）；Gen2-IC 的 Qwen 变体在 <0.05 bpp 于 PSNR/LPIPS/DISTS 及 OCR/人脸 ROI 语义指标全面领先（paper:arxiv:2606.21030）；Gen2-VC 匹配 LPIPS 下相对 VTM-23.0 平均节省 86.65% 码率（匹配 DISTS 94.24%），LoRA 适配器免重训跨 DCVC-RT/ECM/VTM/HM 泛化（paper:arxiv:2609.34725）。

**（b）对指标自身的批判性研究**：
- 扩散 VSR 主观对齐检验：LPIPS、DISTS、CVQA-FR 等 CNN 全参考模型与主观分数相关性显著高于传统 FR 与所测 NR 模型，但**多数被测模型会高估 SCST 产生的过锐结果**，最佳 CNN-FR 模型仍不足以替代主观测试（paper:arxiv:2605.25940）；
- 结构性限制：SSIM/MS-SSIM/LPIPS/DISTS/WD 均以完整解码图为输入、**不可按块分解**，无法进入编码内循环；IDQD-RDO 用随机 Hessian 二次化近似实现块级 RDO，五种 FR-IQA 目标（含 LPIPS）在 VVC 上 BD-rate 节省 14.2–36.7%，代价为编码端复杂度 +10–30%（paper:arxiv:2609.30077）；
- 语义保真盲区：LPIPS/DISTS 感知损失可改善真实感但**不保证语义级保真**，典型症状为文字损坏与人脸身份漂移（paper:arxiv:2606.21030 精读）。

**（c）变体与无参考化**：医学超声领域提出基于超声基础模型的 uLPIPS，与分割语义损伤（Dice 下降）的校准优于 VGG-LPIPS 基线，专家偏好预测准确率由 47.2% 提升至 72.8%（paper:arxiv:2604.19512）；ISP 流水线评估中以代理参考图无参考估计 PSNR/SSIM/LPIPS，优于直接指标回归（paper:arxiv:2607.23321）。

**（d）作为可建模的设计变量**：分层离散视频压缩中，对数线性模型（R²=0.82）显示码本容量 K 主导 LPIPS（α=−0.0094，t=−6.6，p<0.001）而空间分辨率不显著（β=−0.0009，t=−0.43，p=0.68），每对数单位影响比约 10×；同等或更低码率下 LPIPS 相对 H.264 增益 25–52%（128×128）、相对 H.265 增益 21–37%（256×256）（paper:arxiv:2607.23366）。

**（e）应用面横向扩展**：语义通信（PVSC 在 LPIPS 可比点相对 VTM+5G LDPC 带宽节省约 75%，paper:arxiv:2605.19397）；免熵编码 LIC（EF-LIC 在 Kodak 以 LPIPS 口径相对 MS-ILLM 最高降码率 67.86%，paper:arxiv:2605.23323）；事件引导视频编码（ENVC 以 LPIPS 口径相对 DCMVC 六基准平均 BD-rate 节省 67.63%，paper:arxiv:2610.02265）；4K 2D 高斯泼溅实时压缩 LPIPS 率失真超 H.265 及学习式方法（paper:arxiv:2609.14129）；退化分类体系以 PSNR/SSIM/LPIPS 量化严重度（paper:arxiv:2605.15906）；UI-LIC 开源评测框架将 LPIPS 纳入标准四指标（paper:arxiv:2606.23545）；世界模型评估（ForgeWM 取被评估系统中最低参考 LPIPS，paper:arxiv:2608.14022）；修复/超分（Fill2SR 在 DIV2K/LSDIR 合成基准取最佳 LPIPS，paper:arxiv:2609.33582；Wonder 4 在 DIV2K×4/×8、Flickr2K×4 取最优 LPIPS/DISTS/NIQE，paper:arxiv:2611.05294；ClearGS 在多数退化设置降低 LPIPS，paper:arxiv:2609.31509）。

**LPIPS 口径量化结果速览**：

| 条目 | 对比对象 | 口径 | 结果 |
|---|---|---|---|
| paper:arxiv:2405.20032 | VAE / H.265 | 极低码率 LPIPS 绝对改善 | 0.139 / 0.118 |
| paper:arxiv:2505.08281 | SOTA 扩散压缩 | LPIPS BD-rate | −80.7% |
| paper:arxiv:2511.06953 | GSVC | LPIPS BD-rate（最大） | −72.1% |
| paper:arxiv:2601.10373 | SOTA 扩散压缩 | LPIPS BD-rate | 节省 27.2% |
| paper:arxiv:2604.08329 | HEVC | BD-LPIPS（<0.05 bpp） | 0.214 |
| paper:arxiv:2605.19397 | VTM+5G LDPC | LPIPS 可比点带宽节省 | ≈75% |
| paper:arxiv:2605.23323 | MS-ILLM（Kodak） | LPIPS 口径最大码率降低 | 67.86% |
| paper:arxiv:2607.22772 | GLVC | 匹配 LPIPS 平均码率节省 | 62.5% |
| paper:arxiv:2609.34725 | VTM-23.0 | 匹配 LPIPS 平均码率节省 | 86.65% |
| paper:arxiv:2610.02265 | DCMVC | LPIPS BD-rate（六基准平均） | 67.63% |
| paper:arxiv:2609.30077 | VVC 基线 | 含 LPIPS 的 FR-IQA 目标 BD-rate | 14.2–36.7% |

---

## 当前状态与关注点

**活跃度**：2026 年单年 23/33 条（约 70%），月均约 2 条，处于档案观测期内峰值；生成式视频压缩、极低码率（<0.05 bpp）区间与 3DGS 系表示是 2026 年三大增量来源。

**生态位**：已从"与 PSNR/SSIM 并列的感知补充指标"演变为生成式压缩社区的主报点口径——SOTA 声明（GLVC、YODA、ZeroGVC）、BD-rate 轴（ResULIC/GFix/ENVC）、跨方案等质量比较锚点（PVSC、GenVC、Gen2-VC）均以其为基准单位；同时与 DISTS/FID/KID/DOVER 成组报告已成惯例，单一 LPIPS 报点在档案内几乎不出现。

**开放问题**：
1. **感知对齐天花板**：WD 在优化目标与人类评分预测（Pearson >94%）上均优于 LPIPS（paper:arxiv:2412.00505）；扩散 VSR 场景多数质量模型（含 LPIPS 类）高估过锐结果且不足以替代主观测试（paper:arxiv:2605.25940）。
2. **语义保真盲区**：LPIPS/DISTS 无法约束文字、人脸身份等语义级保真（paper:arxiv:2606.21030），需与 OCR CER/WER、人脸 ROI 相似度等互补——语义指标可能成为下一个口径竞争者〔档案推断〕。
3. **不可分性与工程内嵌**：块级 RDO 需依赖 Hessian 二次化近似且引入 10–30% 编码端开销（paper:arxiv:2609.30077），LPIPS 进入编码内循环尚无无损方案。
4. **领域骨干依赖**：VGG 骨干在超声等非自然图像域校准不足，催生领域基础模型骨干的 uLPIPS（paper:arxiv:2604.19512）与无参考代理估计（paper:arxiv:2607.23321）。
5. **口径混杂**：BD-rate 节省、匹配质量码率节省、绝对 LPIPS 改善、相对改进幅度（如 286.53%）多种口径并存，跨论文横向比较需显式对齐口径。

**档案管理注记**：paper:arxiv:2610.06196（EORestore-Agent）挂接于本档案，但其摘录以 PSNR 为修复决策与评测口径，未见 LPIPS 显式使用记录，建议复核挂接依据。
