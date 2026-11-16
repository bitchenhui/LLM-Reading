# MS-SSIM · 实体档案

> metric:MS-SSIM · 数据截止 2026-11-16 · 关联 26 条 · glm-5.3

# 滚动档案：MS-SSIM（metric:MS-SSIM）

## 档案概览

- **实体身份**：质量度量，方向为**越高越好**（注册表静态信息）。归类为全参考图像质量评估（FR-IQA）度量，与 SSIM、LPIPS、DISTS、WD 同列 [paper:arxiv:2609.30077]；命名含义为多尺度结构相似度〔档案推断：由缩写惯例推得，库内无算法定义条目〕。
- **档案构成**：挂接条目 26 条，时间跨度 2021-11-29 → 2026-10-26；论文 23 篇、JVET 提案 2 项、软件版本发布 1 次。
- **在本档案语料中承担的五类功能角色**：
  1. **等质量锚点 / 码率节省口径**：固定 MS-SSIM 水平比较码率 [paper:arxiv:2111.14474][paper:arxiv:2411.19442]；
  2. **RD / BD-rate 评测轴**：与 PSNR 并报的常规质量指标 [paper:arxiv:2304.02273][paper:arxiv:2312.15829]；
  3. **训练 / 优化目标**：作为损失或感知优化目标 [paper:arxiv:2305.02145][paper:arxiv:2401.11615][paper:arxiv:2607.10478]；
  4. **生产编码器 tune 模式**：SVT-AV1 显式调优选项 [repo_release:github:SVT-AV1-v4.0.0]；
  5. **标准化评测指标**：JVET 超分辨率实验与 JPEG AI 标准验证 [standard_proposal:jvet:m195-AE0162][paper:arxiv:2510.13867]。
- **结构性技术前提**（多份资料的共同论据）：以完整解码图像为输入、**不可按块分解**，与块级拉格朗日 RDO 不兼容，无法进入编码内循环 [paper:arxiv:2608.07799][paper:arxiv:2609.30077]；相较 MSE/PSNR 主观相关性更好，但代价是损失可加性与块级独立性 [paper:arxiv:2608.07799]。

## 关键事实与演进

### 2021–2023：学习式编码的等质量锚点；度量实现治理首次进入标准组织

- **2021-11** JCEVC 首次在档案中体现 MS-SSIM 的"口径杠杆"作用：相同 PSNR 下较 x265 LDP very fast 平均降 bpp 39.39%，而**相同 MS-SSIM 下降幅扩大至 54.92%**——感知口径下的码率节省系统性大于保真口径 [paper:arxiv:2111.14474]。
- **2023-04** MMVC 将 PSNR 与 MS-SSIM 并列作为学习式视频压缩的常规评测双口径 [paper:arxiv:2304.02273]。
- **2023-05** ProgDTD 将 MS-SSIM 用作渐进式学习图像压缩的优化/评测目标，渐进化后 MS-SSIM 性能与非渐进对应模型持平 [paper:arxiv:2305.02145]。
- **2023-07（度量治理事件，本档案中唯一直接针对 MS-SSIM 计算本身的修正记录）**：JVET AE 会议同期出现两份提案——AE0162（AHG11/AHG14）指出**超分辨率评测中 MS-SSIM 计算存在错误/偏差并给出修正** [standard_proposal:jvet:m195-AE0162]，AE0230 对该修正做交叉核验 [standard_proposal:jvet:m195-AE0230]。表明该指标的实现细节（尤其涉及分辨率变化的 SR 场景）足以影响标准化实验结论，需专门修复与验证。
- **2023-09** 快速学习图像编码方案在 Kodak 与 Tecnick-40 上以 PSNR 与 MS-SSIM 双指标超越 H.266/VVC-intra(4:4:4) [paper:arxiv:2309.02529]。
- **2023-12** MaskCRT 呈现典型分化形态：PSNR-RGB BD-rate 与 VTM-17.0 低时延 P 仅"相当"，**MS-SSIM-RGB 上优于 VTM-17.0**——学习式编码器对传统锚点的超越常先在 MS-SSIM 轴上成立 [paper:arxiv:2312.15829]。

### 2024：口径分化被量化；基准设施化；主观相关性首次受到直接挑战

- **2024-01** CLIC（上下文聚类）量化了两种不对称性中最强的一种：**MSE 优化**下较 VVC 节省约 10% BD-rate（三个常用基准），**MS-SSIM 优化**下节省超过 50%——优化目标与评测口径的匹配会主导 BD-rate 结论 [paper:arxiv:2401.11615]。
- **2024-01** 结构-细节分解帧间编码器在全部常用测试集上 PSNR 与 MS-SSIM 均优于 H.266/VVC 参考软件 [paper:arxiv:2401.15864]；**2024-03** S2LIC 报告超越 VTM-17.1（条目摘要未含显式 MS-SSIM 数值〔档案推断：挂接源于其 RD 评测使用〕）[paper:arxiv:2403.14471]；**2024-07** BiSIC 在立体图像压缩上 PSNR 与 MS-SSIM 超越传统及学习式方法 [paper:arxiv:2407.10632]。
- **2024-09（基准设施化）**：USTC-TD 测试数据集（40 张 4K 图像 + 10 个 1080p 视频）以 **PSNR/MS-SSIM/VMAF/MOS** 四指标建立标准化与学习型编码方案基准，并被 IEEE VCIP 2022/2023 端到端编码挑战赛实际采用——MS-SSIM 被制度化为公共基准指标之一 [paper:arxiv:2409.08481]。
- **2024-11** MCUCoder 以 MS-SSIM 为质量口径定义"同质量"：能耗相近条件下较 M-JPEG 码率降低 55.65%（MCL-JCV）/ 55.59%（UVG），指标下沉到 MCU 级资源受限场景 [paper:arxiv:2411.19442]；DeepFGS 及其引用的 MLiC 延续"PSNR/MS-SSIM 全面超越传统编码器"的表述惯例 [paper:arxiv:2412.00437]。
- **2024-11（竞争性挑战）**：Ballé 等的过拟合压缩研究显示，**Wasserstein 失真对人类评分的预测能力优于 LPIPS、DISTS 与 MS-SSIM**（WD 与人类 Elo 分数的 Pearson 相关系数 >94%；MS-SSIM 具体数值未给出）——档案中首次出现 MS-SSIM 主观预测能力被超越的直接证据 [paper:arxiv:2412.00505]。

### 2025：进入正式标准化验证；双口径 BD-rate 常态化

- **2025-02 / 2025-08** FD-LSCIC（屏幕内容，PSNR 与 MS-SSIM 均超传统标准与 SOTA）[paper:arxiv:2502.15174]、HyTIP（PSNR-RGB 与 MS-SSIM-RGB 均优于 VTM 17.0 Low-delay B）延续双口径报告 [paper:arxiv:2508.02072]。
- **2025-10（标准化里程碑）**：JPEG AI 学习型图像编码标准首版（计划 2025 年初完成）以 **MS-SSIM、FSIM、VIF、VMAF、PSNR-HVS、IW-SSIM、NLPD** 七项指标族验证相较现有标准的显著 BD-rate 降低——MS-SSIM 进入正式国际标准的验证指标集 [paper:arxiv:2510.13867]。
- **2025-12** NVRC-Lite 按口径分别报告 BD-rate 节省（相对 C3，最大值）：PSNR 口径 21.03%、**MS-SSIM 口径 23.06%**，双口径分报成为神经表示压缩的常规做法 [paper:arxiv:2512.04019]。

### 2026：进入编码器内循环与生产部署

- **2026-06** InnVC 再次放大口径剪刀差：UVG 上相对 x265，PSNR BD-rate 降 21.66%，**MS-SSIM BD-rate 降 46.06%** [paper:arxiv:2606.13957]。
- **2026-07** 可微 H.264 代理用于自适应量化：以 MS-SSIM 为感知优化目标时，相对固定 QP 基线 **MS-SSIM BD-rate 最高降 15.30%**（语义分割任务口径最高 17.12%）——MS-SSIM 成为梯度可穿越代理后的直接优化对象 [paper:arxiv:2607.10478]。
- **2026-08** 码率分配迁移：用神经模型的感知重要性生成 QP 图，HEVC B~D 上以 MS-SSIM 衡量较 **JM-19.0 省 20.20%、HM-16.20 省 8.25%、VTM-23.0 省 8.37%**；其动机陈述再次确认 MS-SSIM 因不可分解而无法进入块级 RDO 的结构性障碍 [paper:arxiv:2608.07799]。
- **2026-09（内循环破壁）**：IDQD-RDO 将含 MS-SSIM 在内的五种 FR-IQA 度量近似为输入相关二次失真（随机 Hessian 估计），实现 VVC 块级 RDO，**五种目标度量下 BD-rate 节省 14.2–36.7%**（Kodak 与 CLIC；未给 MS-SSIM 单项分解），编码端额外开销 10–30%、解码器无变化 [paper:arxiv:2609.30077]。同期 Gen2-VC（LoRA 生成先验增强）据称为首个低码率下 **PSNR 与 MS-SSIM 均优于 VTM-23.0** 的生成式视频编码器（六数据集 BD-rate 均值）；其最大码率节省出现在匹配 LPIPS（86.65%）与 DISTS（94.24%）时而非 MS-SSIM 口径 [paper:arxiv:2609.34725]。VQ-LIC（FPGA 学习图像压缩）同日挂接，摘要不含显式 MS-SSIM 结论〔档案推断：挂接源于评测使用〕[paper:arxiv:2609.29727]。
- **2026-10（生产部署里程碑）**：SVT-AV1 v4.0.0（含破坏性 API 更新、CRF 扩展至 70 并支持四分之一粒度步进）中，**AVIF 与静图模式在 tune MS-SSIM 下同质量 M11–M0 提速约 5–8 倍，同等复杂度下 BD-Rate 改善约 5–8%**——MS-SSIM 作为显式调优目标存在于大规模部署的开源编码器发布线中 [repo_release:github:SVT-AV1-v4.0.0]。

## 当前状态与关注点

- **活跃度**：2021–2026 连续六年无间断挂接；角色已从"论文评测指标"扩展至"标准验证指标（JPEG AI）[paper:arxiv:2510.13867]、标准组织度量修正对象（JVET）[standard_proposal:jvet:m195-AE0162]、生产编码器 tune 模式 [repo_release:github:SVT-AV1-v4.0.0]、编码器内循环优化目标 [paper:arxiv:2609.30077]"。最近条目为 2026-10 版本发布，处于活跃周期。
- **开放问题**：
  1. **实现正确性**：JVET-AE0162/0230 表明 SR 等分辨率变化场景下 MS-SSIM 计算存在需专门修复与交叉核验的错误源 [standard_proposal:jvet:m195-AE0162][standard_proposal:jvet:m195-AE0230]；档案内无后续采纳状态记录，属未闭环事项。
  2. **主观相关性天花板**：WD 对人类评分的预测优于 MS-SSIM（Pearson >94%，MS-SSIM 数值未披露）[paper:arxiv:2412.00505]；生成式编码器的最大感知收益由 LPIPS/DISTS 口径捕获而非 MS-SSIM [paper:arxiv:2609.34725]——面向生成式压缩时该指标的区分力存疑。
  3. **RDO 结构性障碍的解法竞争**：2026 年三条路线并行——可微代理 AQ [paper:arxiv:2607.10478]、码率分配迁移 [paper:arxiv:2608.07799]、Hessian 二次近似 IDQD-RDO [paper:arxiv:2609.30077]，均以 MS-SSIM 类感知度量为目标，尚未见相互对比或标准化采纳记录。
  4. **口径敏感性与可比性**：同一系统在 MS-SSIM 口径下的优势系统性大于 PSNR 口径（54.92% vs 39.39% [paper:arxiv:2111.14474]；46.06% vs 21.66% [paper:arxiv:2606.13957]；23.06% vs 21.03% [paper:arxiv:2512.04019]），且优化目标与评测口径匹配可造成 >50% vs ~10% 的 BD-rate 差异 [paper:arxiv:2401.11615]〔档案推断：跨论文比较时必须同时声明优化目标与评测口径，否则结论不可比〕。
- **生态位**：居于 PSNR（保真、RDO 兼容、主观相关性弱 [paper:arxiv:2608.07799]）与 LPIPS/DISTS/WD（深度感知度量）之间的中间层；已被基准套件（USTC-TD 四指标之一，VCIP 挑战赛采用 [paper:arxiv:2409.08481]）与国际标准验证（JPEG AI 七指标族 [paper:arxiv:2510.13867]）制度化，且保有生产编码器级支持 [repo_release:github:SVT-AV1-v4.0.0]，短期内不可替代。
- **档案缺口与跟踪建议**：① 无 MS-SSIM 算法本体定义条目（尺度数、权重、色彩处理），JVET 修正事件提示实现细节敏感，建议补充；② JVET AE0162 修正的后续采纳情况未跟踪；③ IDQD-RDO 等内循环集成方法是否进入标准编码器（VTM/JEM 系）待观察；④ 与机器视觉任务口径（BD-task）的联合使用趋势已现 [paper:arxiv:2607.10478]，可设交叉观察点。
