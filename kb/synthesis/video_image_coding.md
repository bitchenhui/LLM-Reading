# 视频/图像编码 · 领域综述

> 引擎合成 · 数据截止 2026-11-14 · 基于 126 条结构化条目 · glm-5.3

# 视频/图像编码领域综述（数据截至 2026-11-14，共 126 条）

> 本综述基于知识库 126 条条目（74 篇论文 + 52 条版本动态）。需说明语料结构特征：版本动态覆盖 2016–2026 年传统/开源编解码器演进全程，而论文条目集中于 2026 年 1–11 月，故「发展历程」以版本里程碑为骨架、「技术主线」以 2026 年研究前沿为主体。

---

## 一、发展历程

### 阶段一（2016–2018）：开源 HEVC 编码器工程化成熟

开源 HEVC 编码器 Kvazaar 完成了从可用到高效的跨越：v1.0.0 经全预设率失真-复杂度搜索重优化，veryslow 档平均提速约 12.42×（官方口径约 10×），中高速预设 3-fr 档 BD-rate 较 v0.8.3 降 31.0%，并引入无损编码、单色、--crypto 码流选择性加密与 4×8 SMP/4×12 AMP 分割（repo_release:github:kvazaar-v1.0.0）。v1.1.0 将码控细化到 LCU 级并新增 ROI delta-QP（repo_release:github:kvazaar-v1.1.0）；v1.2.0 全预设提速 1.19–1.28×，最快档 BD-Bitrate 降 14.80%（hevc-B 0-uf 达 19.04%），并率先引入 360° ERP 自适应 QP（--erp-aqp）与帧内预测模式加密（repo_release:github:kvazaar-v1.2.0）。同期 dav1d 0.1.0 'Gazelle'（2018-12）确立 AV1 解码侧轻量高性能基线：全特性、8–12bit、全色度子采样，AVX-2 上显著快于其他 AV1 解码器，且首发即带 SSSE3/NEON 汇编（repo_release:github:dav1d-0.1.0）。

### 阶段二（2019–2021）：HEVC 效率深挖与架构升级

Kvazaar v1.3.0 以预设间速度换压缩——0-uf 档 BD-Bitrate 降 22.7% 但 8-vs 档减速至 0.35×——并引入 --rd=2 的 SSD 度量、CU 级 QP 信令与低延迟 B 帧 GOP（repo_release:github:kvazaar-v1.3.0）。v2.0.0 是十年间最大效率跃迁：新增 OBA（optimal bit allocation）码控与方差自适应量化 VAQ，各速度档 BD-Bitrate 较 v1.3 平均降 15.4%–31.1%（hevc-D@2-vf 达 -37.4%），并将机器学习用于帧内 PU 深度约束（--ml-pu-depth-intra）（repo_release:github:kvazaar-v2.0.0）。v2.1.0 转向 BSD-3 许可证并补齐 AVX2 插值与 Y4M 输入（repo_release:github:kvazaar-v2.1.0）。

### 阶段三（2022–2024）：VVC 开源工具链成型与跨平台化

解码侧，vvDec 自 v2.1.0 起引入首批原生 ARM SIMD 并完成 CU=PU 重构（repo_release:github:vvdec-v2.1.0），随后连续修复 RPR 越界读取（repo_release:github:vvdec-v2.1.2）、降低 RPR 填充（repo_release:github:vvdec-v2.1.3）；v2.2.0 通过 simd-everywhere 启用 AVX2→NEON 转译、解除 64 线程限制并优化播放能效（repo_release:github:vvdec-v2.2.0）。v3.0.0（2024-10）为破坏性 API 版本，新增胶片颗粒支持并从 VVenC 回移植 ARM SIMD（repo_release:github:vvdec-v3.0.0）。编码侧 VVenC v1.12.0 引入封顶恒定质量模式 CQF 与自动多线程配置（repo_release:github:vvenc-v1.12.0）；v1.13.0 面向 DASH 引入 idr_no_radl 刷新模式、GOP 自适应 QP 级联与实验性胶片颗粒分析，medium 预设提速约 5%（repo_release:github:vvenc-v1.13.0）。Kvazaar 同期以 v2.2.0（逐帧 ROI 映射、搜索中更新 CABAC 上下文，8-vs 档 BD-rate 降 5.6%，repo_release:github:kvazaar-v2.2.0）与 v2.3.x 系列持续做 AVX2 微优化（repo_release:github:kvazaar-v2.3.0；repo_release:github:kvazaar-v2.3.1）。图像侧 libavif 在 2024 年完成实验性增益图与分层 AVIF 的引入（repo_release:github:libavif-v1.1.0）并修复安全内存错误，2025 年 v1.2.0 将增益图 API 转正、支持 YCgCo-R、弃用旧量化器参数（repo_release:github:libavif-v1.2.0）。

### 阶段四（2025–2026.10）：生产化强化与 SVT-AV1 快速迭代

VVenC v1.13.1 将 x86 最低指令集提至 SSE 4.1 并修复 slice type adaptation 下的码控精度缺陷（repo_release:github:vvenc-v1.13.1）；v1.14.0（2026-01）完成大规模 ARM NEON/SVE 优化且硬件支持时默认启用 SVE，同时弃用 LMCS、cts/dts 改为有符号整数（repo_release:github:vvenc-v1.14.0）。vvDec v3.1.0 新增 Loongarch 支持与 opaque userData 指针（repo_release:github:vvdec-v3.1.0）；v3.2.0 补齐 NEON-RDM/SVE/SVE2 并引入 libfuzzer 模糊测试基础设施（repo_release:github:vvdec-v3.2.0）；v3.2.1 修复五个安全漏洞（含 ALF APS use-after-free、SPS 整数溢出等）（repo_release:github:vvdec-v3.2.1）。Kvazaar v2.3.2（2025-09）通过修复 10-bit 与 SMP/AMP 代价计算 bug 使 veryslow 档相对 v2.3.1 BD-BR(PSNR) 降 2.7%（速度 0.77×）（repo_release:github:kvazaar-v2.3.2）。SVT-AV1 在 2026-10 至 11 月密集发布 v3.0.1–v4.3.0：v3.1.0 新增 --rtc 模式（RTC 场景 BD-Rate 改善约 5–10%，随机接入提速 15–25%）（repo_release:github:SVT-AV1-v3.1.0）；v4.0.0 为破坏性 API 版本，AVIF/静图模式提速 5–8×、CRF 扩展至 70 并引入 AC Bias 心理视觉特性（repo_release:github:SVT-AV1-v4.0.0）；v4.2.0 新增 TUNE-VMAF（目标约 15% VMAF BD-rate 改进）与 RTC CBR 码控（卡尔曼滤波 QP 估计）（repo_release:github:SVT-AV1-v4.2.0）；v4.3.0 全 preset 效率再提升 5–8% 并新增 --fast-decode 3 与胶片颗粒表 API（repo_release:github:SVT-AV1-v4.3.0）。libavif v1.4.x 落地 AVIF v1.2 Sample Transform、AOM_TUNE_IQ 默认调优与渐进/分层特性转正（repo_release:github:libavif-v1.4.0；repo_release:github:libavif-v1.4.1）。

### 阶段五（2026）：神经与生成式编码研究集中爆发

2026 年论文条目呈现三条并行加速线：其一，神经视频编码进入部署攻坚——NPU 跨平台一致性（paper:arxiv:2606.28027）、混合精度整数化（paper:arxiv:2606.13110）、AVS NVC 标准化采纳 skip 模式框架（paper:arxiv:2611.00181）；其二，生成式压缩从多步扩散走向一步/少步与零样本（paper:arxiv:2601.01141；paper:arxiv:2606.22371；paper:arxiv:2607.28144）；其三，标准化侧 AV2 完成变换与熵编码设计文档化（paper:arxiv:2601.02712）并给出 CTC 实测增益（paper:arxiv:2605.15800）。

---

## 二、技术主线与代表工作

### 主线 1：传统混合编码的工具级优化（VVC/AV2/ECM）

- **AV2 标准设计**：在 AV1 基础上重新设计变换核并引入 IST、TCQ、ATC、PARA、FSC、CCTX、PH 等变换/量化/熵编码工具（paper:arxiv:2601.02712）；AV2 CTC 实测 AV2 v13.0 相对 AV1 在随机访问配置下 PSNR-YUV 节省 29.81%、VMAF 节省 33.79%，且标准立项即约束编码器复杂度增幅 ≤5×、解码器 ≤2×，CTC 采用 6 个 QP 点并首次纳入 UGC 与自适应流配置（paper:arxiv:2605.15800）。
- **变换侧加速**：FaSST 以 Givens 旋转分解构造快速二次变换，模式自适应版本在匹配 LFNST 率失真性能的同时计算量减少 83.67%，避免固定系数截断后最高可再获 1.80% BD-rate 节省（复杂度降 66.24%）（paper:arxiv:2605.15086）。
- **划分搜索加速**：VVC 的 QTMTT 使 64×64 intra CTU 全 RDO 候选块数从 HEVC 的 341 个膨胀至 721×10³ 个（最坏情形约 2000×/1000× 于 HEVC），领域综述指出划分加速方法需随 VTM 内部启发式演进持续适配、单点 trade-off 报告范式已不充分（paper:arxiv:2605.21526）。HEVC 侧 HFViT 以重参数化深度可分离卷积 + carrier token 层级注意力在近 CNN 级 CPU 延迟下将 VMAF BD-rate 惩罚较 ETH-CNN 基线降低 2.4–7.9 个百分点（Class A/B/E）（paper:arxiv:2605.29063）。
- **帧间工具加速**：基于 2-tap 滤波器差分近似将 VVenC MMVD 候选判决降为一次残差-梯度内积，fast 预设下以 2.23% 时间节省获得 -0.35% BD-rate（相对 full MMVD 的 -0.64%/21.10%），效率-复杂度比 η 从 11.79 降至 7.10（paper:arxiv:2606.31084）。
- **环路滤波**：以多项式图滤波器替代 ECM 细粒度梯度分类固定滤波（56×8×16=7168 类别映射至 512 个滤波器），滤波器数量减少一个数量级且性能相当（paper:arxiv:2607.04985）。
- **中间码/特殊场景**：HLC 以无数据依赖调色板设计实现高吞吐 palette 模式，相同吞吐（4K@120fps）下 LUT 资源仅为 JPEG-XS 编码器一半，文字内容 BD-PSNR 增益最高 5.312 dB（paper:arxiv:2603.29864）；商用 GPU 四路分帧实现 8K 10-bit 4:2:2 HEVC 编码 122 fps 支撑 V-PCC 体积视频流，代价是最高 5% 的 BD-rate 惩罚（paper:arxiv:2606.29179）。

### 主线 2：学习式图像压缩（LIC）——熵建模与复杂度

- **外部先验熵建模**：HiDE 以全局-局部双字典级联检索引入外部先验，相对 VTM-12.1 在 Kodak/CLIC/Tecnick 分别节省 18.5%/21.99%/24.01% BD-rate（paper:arxiv:2603.06766）；ARCHE 在纯卷积框架内统一层级超先验、空间自回归与通道条件化并嵌入 SE 激励与潜残差预测，Kodak 上相对 VVC Intra 降约 5% BD-Rate（95M 参数、单图 222ms，无 Transformer/循环组件）（paper:arxiv:2603.10188）；ChWDTA 将通道级小波变换置于窗口注意力 Q/K/V 投影之前并配套小波包切片熵模型，八切片配置下三个测试集 BD-rate 降 17.82%–22.56%（paper:arxiv:2606.00111）。
- **训练正则**：编码器输入端注入高斯噪声作为结构化正则（率侧为信息加权 Jacobian 惩罚、失真侧为 Frobenius 收缩惩罚），复现 ELIC 骨干即获 -2.60% BD-rate，DMCI-Large 相对 VTM-22.0 达 -22.02%（paper:arxiv:2611.10073）。
- **诊断基准**：DCT 单频探针实验揭示 BMSHJ/MBT/Cheng2020 在约 1bpp 工作点的高频重建能量有 80–97% 泄漏到目标频带之外（目标频率增益仅 0.02–0.23），仅解码器微调即可在码流固定前提下将八种架构泄漏能量降低 90–99.8%（Kodak PSNR 代价 0.09–0.59 dB）（paper:arxiv:2611.10000）。
- **低复杂度与弹性**：多编解码器空间竞争在解码复杂度仅 1433 MACs/pixel 下达到 HEVC 水平性能、相对单一编解码器最多省 14.5% 码率（paper:arxiv:2605.13243）；通道级掩码引导的非连续通道选择相对同宽度 Slimmable 基线在 w=48 下省 19.22%–24.11% BD-rate，单一 VBR 模型可替代 40 个独立模型（存储缩减 14.8–15.9×）（paper:arxiv:2610.27037）；渐进式编码 BLI 将三态平面编码重构为区间收缩下的序贯隐变量推断，Kodak 上相对 DPICT 降 17.78%、参数量约为 CTC 的 1/5.3（paper:arxiv:2610.30966）。部署综述以 TinyLIC 基准给出锚点：约 10 KMACs/pixel 显著优于 HEVC 图像档、50 KMACs/pixel 匹配 VVC 图像档（paper:arxiv:2610.22421）。

### 主线 3：神经视频编码（NVC）——从 RD 竞争到部署

- **架构统一**：Uni-LVC 提出「inter = 以时域特征为条件的 intra」，单模型覆盖 AI/LD/RA，并以可靠性感知分类器在参考不可靠时（如场景切换）退化为帧内主导（paper:arxiv:2603.05756）；InnVC 以可逆主变换路径 + 隐式条件场实现 >20 dB PSNR 跨度的宽质量覆盖，UVG 上相对 x265 PSNR BD-rate 降 21.66%、MS-SSIM 降 46.06%（paper:arxiv:2606.13957）；HR-NVC++ 以置信度引导的双向时域线索 + 空间补充分支统一 UHD 编码，UVG-4K 与 JVET A1/A2 上 RA 配置相对 VTM-13.2 平均省 13.01% PSNR BD-rate，且单一共享上下文同时支撑保真/感知双模式（paper:arxiv:2611.15670）。
- **解码加速与部署**：KD-NVC 以两阶段搜索-蒸馏在 RTX 5060 上实现 1080p 69 FPS 解码且 RD 与 VTM-LDB 相当（paper:arxiv:2606.04595）；MLVC 通过 Scale Sending（σ 由固定 factorized 熵编码的 hyperlatent 显式导出）+ ReLU 系激活 + LTR 恢复帧，首次在 Apple/Intel/Qualcomm NPU 上稳定运行神经视频编码，VCD 会议视频基准 MOS 口径相对 HEVC-QSV BD-rate 提升超 70%（paper:arxiv:2606.28027）；JOMP 将量化参数与位宽同设为可学习变量并构建完整整数化流水线，率失真对标 DCVC-FM 前提下位操作减少 87.6%（paper:arxiv:2606.13110）。
- **码控与可控性**：反馈驱动码控以 log 域 PI/PID 闭环 + 双分支 GRU 调节器实现 DCVC 上平均码率误差 2.88%（加 GRU 后 2.13%）同时 BD-rate 再降 5.69%（paper:arxiv:2604.20104）。
- **特殊模态与场景**：事件引导的 ENVC 利用编解码两端共享的事件流构建运动先验，六个基准上相对 DCMVC 平均省 39.13%（PSNR）/ 67.63%（LPIPS）BD-rate（paper:arxiv:2610.02265）；静态场景 PIC 将短期时变重释为正向激励噪声微调 NVC，在 0.009% 压缩率下视觉无损，DCVC-FM 需高 20.5% 码率才达相当质量（paper:arxiv:2603.06095）；神经无损视频压缩 NeuralLVC 以掩码扩散 + 时间条件化在 CIF/720p/1080p 全分辨率超越 H.264/H.265 无损模式，P 帧参考嵌入仅增 1.3% 参数（paper:arxiv:2604.03353）。
- **标准化接口**：率失真优化跳过模式框架 RDOSkip 实现推理期即用、免训练，AVS 数据集省 0.90%、HEVC 数据集省 1.29% BD-rate，其时域跳过决策已被进行中的 AVS NVC 标准采纳并集成进参考软件（paper:arxiv:2611.00181）。

### 主线 4：生成式压缩——扩散先验与率-失真-感知（RDP）三角

- **一步/少步扩散**：YODA 以时域感知自编码器 + 条件隐变量编码器 + 线性 DiT 一步去噪，在 LPIPS/DISTS/FID/KID 四个感知指标上达 SOTA（paper:arxiv:2601.01141）；图像侧 DiffCR 以频率感知先验精炼 + 轻量一致性估计实现两步解码，相对 SOTA 扩散基线 LPIPS 口径省 27.2%、PSNR 口径省 65.1% BD-rate，解码加速超 10×（paper:arxiv:2601.10373）。
- **从头训练与蒸馏**：GenVC 是首个为压缩从零训练的视频扩散模型，以自适应得分蒸馏（按真值方向对齐度门控 DMD 更新）修复运动停滞，匹配 LPIPS/FID 条件下相对 GLVC 分别省 62.5%/71.3% 码率，模型仅 478M 参数、1080p 单步解码 15.1 fps（A100）（paper:arxiv:2607.22772）。
- **零样本与潜空间传输**：ZeroGVC 以「码本原子索引 + 量化系数」引导预训练自回归视频扩散的少步一致性采样，完全免训练，A800 上达 5–10 FPS（paper:arxiv:2606.22371）；Gen2-IC 以潜空间传输为通用接口挂接 SD-2.1/SANA-1.5/FLUX.1-dev/Qwen-Image 四种骨干，更强先验（Qwen 变体）在 <0.05 bpp 区间全面领先（paper:arxiv:2606.21030）。
- **实时化**：ReGenVC 以神经压缩首帧 + 姿态关键点为码流（77 帧约 26 kB，约为 x264/x265 无伪影所需 250–280 kB 的十分之一），经四步蒸馏与三项系统优化在 8-GPU 节点实现 24 fps 实时输出、25 帧窗口延迟 972 ms（paper:arxiv:2607.28144）。
- **RDP 操作点导航**：DCIC 以幂等约束作为分布感知的可处理代理，双衰减因子 (K_D,K_P) 支持固定码率下从单一比特流连续调节保真-真实感权衡（paper:arxiv:2606.13366）。
- **外挂式生成增强**：Gen2-VC 用仅训练于 DCVC-UF 的 LoRA 适配器在解码侧增强既有编码器（码流与参考帧链零改动），匹配 LPIPS/DISTS 下相对 VTM-23.0 平均省 86.65%/94.24% 码率，且 LoRA 无需重训练即泛化到 DCVC-RT/ECM/VTM/HM（paper:arxiv:2609.34725）。INR 条件化的 DiV-INR 在 <0.05 bpp 极低码率下相对 HEVC 取得 BD-LPIPS 0.214 的提升（paper:arxiv:2604.08329）。

### 主线 5：过拟合/INR 路线

NVRC++ 将表达能力从网络卸载到高分辨率 feature grid（grid 参数 0.35M→100.06M、MAC/pixel 87.3→24.8、解码 35.5→162.9 FPS），四档复杂度 S1–S4（7.3/25.1/92.5/357.7 kMAC/pixel）单配置覆盖全码率区间，S3 与 NVRC 性能相当但解码快 7.6×（paper:arxiv:2606.28163）；S-NVRC 以特征网格粗到精前缀实现码率可扩展、网络层嵌套前缀实现复杂度可扩展，UVG 上相对 SHM-12.4 省 43.7%、相对多层 VTM-20.0 省 5.6%（paper:arxiv:2609.04273）；图像侧 MIRC 将 NVRC 式端到端量化-熵编码流水线移植到单图并以跨阶段参数共享多尺度表示摊销参数，CLIC2020 专业验证集相对 VTM 22.0 省 10.5%，解码复杂度 1.2–2.9 kMAC/pixel（paper:arxiv:2609.04274）。Cool-chic 系持续演进：LANCE 引入前向传输空间超先验实现熵模型区域自适应（相对 Cool-Chic 4.0 省 1.40–2.99% BD-rate，解码复杂度区间 606–1483 MAC/pixel）（paper:arxiv:2605.20672）；N-O Cool-chic 以编码器网络绕过逐图过拟合，编码复杂度降约 1000× 同时保留约 2000 次乘法/像素的轻量解码（paper:arxiv:2607.13723）。屏幕内容专用 NeR-SC 以可学习调色板与零开销帧跳过在 VCD 数据集低码率超越 H.264/H.265（paper:arxiv:2605.27024）。

### 主线 6：面向机器与语义的编码

WA-RDO 以包装器感知加权 SSE 改造内部编码器比特分配，使 HEVC 级联 FCM 追平基于 VVC 的最优方法、弥合一代编码器代差（paper:arxiv:2601.22070）；MT-JRD 构建 27,264 条标注的多任务恰可辨识差异数据集，属性辅助预测模型使 VCM 相对 VVC/JPEG 基线分别取得 3.861%/7.886% BD-mAP 增益（paper:arxiv:2604.09421）；MoECodec 将 transformer LIC 的 FFN 替换为 Expert-Choice 路由 + GShMLP 专家，单模型服务重建与多机器任务，TIC 主干 Kodak 重建 BD-rate 从 26.98 优化到 15.44（vs VTM-17.1，PSNR），下游分类/检测/分割 BD-rate 为 -7.74/-8.98/-9.72（paper:arxiv:2606.21033）；传感器内 OASIS 以任务置信度闭环反馈在线调节压缩率，平均 6× 压缩、链路功耗降 5.8×、延迟降 2.5×，任务性能退化 ≤1.5%（paper:arxiv:2609.15749）；语义通信 PBSC 取消显式运动矢量传输，相对 VTM+5G LDPC 基线在可比感知质量下最高省约 75%（LPIPS）/87%（DISTS）带宽且单张 RTX 4090 实时（paper:arxiv:2605.19397）。

### 主线 7：感知度量进入编码决策

IDQD-RDO 将 FR-IQA 度量在源图像处二次化（随机 Hessian 估计仅需矩阵-向量积），使 VVC 块级 RDO 在五种目标度量下省 14.2–36.7% BD-rate，编码端开销 10–30%、解码器零改动（paper:arxiv:2609.30077）；无参考指标集成 RDO 以指标集成 + 梯度平滑稳定化解决单 NRM 过拟合与梯度不稳定，在 AVC 与 Cool-chic 上验证（paper:arxiv:2602.15779）；码率分配迁移从 DCVC-FM 蒸馏感知重要性为传统编码器块级 QP 图（解码语法零改动），HEVC B–D 上相对 JM-19.0/HM-16.20/VTM-23.0 分别省 20.20%/8.25%/8.37% MS-SSIM 码率（paper:arxiv:2608.07799）；UGC 转码侧以弱监督 Siamese 排序训练的 Mamba 质量模型作感知损失嵌入 DCVC/HiNeRV 的 RDO，分别省 8.46%/12.89% BD-rate，破解「保真陷阱」（paper:arxiv:2603.25566）；H.264 可微代理驱动的自适应量化在语义分割任务上最高省 17.12% BD-rate、MS-SSIM 省 15.30%（paper:arxiv:2607.10478）。后处理侧 CASR 以 LoRA 低秩过拟合（r=4 最优）预训练超分网络作 VVC 后滤波，相对 VTM21 RA 配置 Y/U/V 分别省 10.93%/15.39%/24.41%（paper:arxiv:2609.37328）。

### 主线 8：码控、码率阶梯与流媒体系统工程

JQT-PF 帕累托前沿框架在保持相同 XPSNR 下相对固定码率梯子平均省 11.76% 码率（激进配置最高 27.88%），JRQT-PF 提供 6.38% 码率节省 + 6.17% 解码时间降低的可控权衡（paper:arxiv:2601.10607）；DQ-Ladder 以深度强化学习构建时间与质量感知阶梯，相对 Apple HLS 阶梯 XPSNR BD-rate 至少降 10.3%、解码时间减 22%，且对最高 20% 预测噪声保持鲁棒（paper:arxiv:2603.13597）；VCA 特征 + 随机森林预测 VVC 帧级比特（I/P/B 帧 R² 分别 0.93/0.88/0.77），嵌入码控回路后效率与 VVenC 两遍码控相当而总编码时间减 33.3%（paper:arxiv:2602.06242）。主观评估方面，LCEVC（LTM 8.1）作为增强层叠加于 HD VVC 基础层，在 MPEG 多层测试方法下以 DCR 方法（25 人、15 个 SDR/HDR 序列、增强层码率占比约 10% 与 50% 两工作点）评估 UHD 感知质量（paper:arxiv:2601.10448）。

### 主线 9：跨域迁移与新载体

- **LLM 权重压缩**：LLMCodec 整合仿射量化与 VVC 编码，LLaMA-3-8B 2-bit 下困惑度较现有方法降低超 1.5×、下游准确率提升 21%（paper:arxiv:2606.05861）。
- **3DGS 编码**：双阶段 Morton 排序将 3DGS 属性转为强局部相关 2D 特征图以复用标准视频编码器，排序速度远快于 PLAS（后者平均耗时 18,698.91 ms）且压缩性能更优（paper:arxiv:2609.29041）；可变形 2DGS 4K 视频压缩框架在 LPIPS 率失真上超越 H.265 及学习式方法并实现实时解码（paper:arxiv:2609.14129）；反向迁移方面，复用 AV1 编码器运动矢量替代穷举特征匹配可使 SfM 初始点云密度最高达经典方法 8×、3DGS 渲染 VMAF +9 分、训练时间减 63%（paper:arxiv:2605.14629）。
- **离散码本容量律**：分层离散视频编码中码本容量 K 对 LPIPS 的每对数单位影响约为空间分辨率的 10×（α=-0.0094 vs β=-0.0009，p<0.001），简化多分辨率部署（paper:arxiv:2607.23366）。

---

## 三、当前关键问题

### 3.1 率-失真-感知三角在超低码率区的结构性张力

RDP 制约使像素保真与感知真实感在低码率下本质冲突（paper:arxiv:2601.01141；paper:arxiv:2606.13366）。生成式路线虽在感知指标上大幅领先（如 Gen2-VC 匹配 LPIPS 下相对 VTM-23.0 省 86.65% 码率，paper:arxiv:2609.34725），但面临三个具体技术风险：其一，**幻觉与内容真实性约束**——监控/会议等场景强制要求像素级保真，生成先验合成的高频细节不可接受（paper:arxiv:2603.06095）；其二，**保真-感知工作点不可同时最优**，DCIC 需引入幂等约束与双衰减因子才能在单一码流上导航 Pareto 前沿（paper:arxiv:2606.13366）；其三，**生成式编解码的语义保真缺口**——文字损坏与人脸身份漂移促使 Gen2-IC 引入 OCR CER/WER 与人脸 ROI 相似度等语义级评测维度（paper:arxiv:2606.21030）。UGC 场景另有「保真陷阱」：参考本身含伪影时保真驱动 RDO 会复刻并强化损伤（paper:arxiv:2603.25566）。DCIC 与 Gen2-VC 分别代表「约束式」与「外挂式」两条缓解路径，但单码流内 RDP 三目标的操作性最优至今未闭合（paper:arxiv:2606.13366）。

### 3.2 神经编解码的跨平台数值一致性与 NPU 部署

这是 2026 年被反复证实的部署级硬约束：熵解码要求编解码两端**逐位一致**的概率分布，而不同厂商 NPU 即便同为 FP16/INT8 也无法逐位复现，一个 index 错位即沿时域预测级联为灾难性失败——DCVC-RT 在 Apple 编/Intel 解场景完全崩溃（paper:arxiv:2606.28027）。MLVC 的 Scale Sending（σ 由固定 factorized 熵编码的 hyperlatent 显式导出）提供结构性解法，但代价是显式传输 scale 的码率开销；JOMP 指出浮点舍入差异污染熵概率估计可致 NaN 溢出与解码失败，其混合精度整数化流水线（位操作减 87.6%）是另一条路，但量化敏感度随编码框架与时域缓冲策略变化、结论尚不可跨 codec 迁移（paper:arxiv:2606.13110）。EF-LIC 则从另一端暴露问题：熵编码串行控制流落在 CPU 上（rANS 单次可超 100 ms），且 GPU–CPU 混合执行阻碍统一计算图导出（paper:arxiv:2605.23323）。

### 3.3 解码复杂度鸿沟与「一次编码、海量解码」范式错配

学习式自编码器解码复杂度普遍超 10⁵ MAC/pixel，与传统编码器存在数量级差距（paper:arxiv:2605.13243）。压缩该鸿沟的方案正在分化：多编解码器空间竞争（1433 MACs/pixel 达 HEVC 水平，paper:arxiv:2605.13243）、TinyLIC 梯度配置（10–50 KMACs/pixel，paper:arxiv:2610.22421）、INR/过拟合路线（Cool-chic 约 2000 次乘法/像素，paper:arxiv:2607.13723）、FPGA 共享 VQ 引擎（0.1945 kMAC/pixel、47.98 fps 硅片实测，paper:arxiv:2609.29727）。但各自遗留问题明确：过拟合路线编码时间问题（N-O Cool-chic 降 1000× 后性能仍逊于全过拟合，paper:arxiv:2607.13723）；空间竞争的模式图边信息开销与编解码器集合训练成本（paper:arxiv:2605.13243）；4K/UHD 下 NVC 帧间对应可靠性随分辨率退化（HR-NVC++ 动机实验，paper:arxiv:2611.15670）。此外**复杂度与码率两个可扩展维度长期耦合**——S-NVRC 首次以网格前缀（码率）+ 网络层嵌套前缀（复杂度）实现双轴独立，但仅限 INR 架构（paper:arxiv:2609.04273）。

### 3.4 传统编码器复杂度控制的方法论危机

VVC 划分搜索候选空间较 HEVC 膨胀约三个数量级（paper:arxiv:2605.21526），而加速方法的评测存在系统性缺陷：现有工作各自锚定单一 VTM 版本与配置，其净贡献可能被「换新版 VTM + 调低 MTT 深度」的零成本操作吞没；JVET 联合 CfE 已要求覆盖多运行时档位的评测（paper:arxiv:2605.21526）。单点工具层面，MMVD 加速揭示了「以解析近似替代完整运动补偿判决」的可行路径（一次内积替代 8-tap 插值+SAD），但 fast 预设下仅省 2.23% 编码时间，说明**预设内部既有快速算法已压缩了可优化空间**（paper:arxiv:2606.31084）。ALF 固定滤波器集合存在严重类别冗余（旋转匹配实验证实系数高度重合），图滤波器减一个数量级后仍有进一步压缩空间（paper:arxiv:2607.04985）。

### 3.5 感知/无参考度量进入块级 RDO 的结构性障碍

FR-IQA 度量不可按块分解（无 SSE 的可加性与 Parseval 等价性），NRM 又是「图→标量」的高度非线性映射且梯度局部不稳定、单一优化会利用模型特有偏差（paper:arxiv:2602.15779）。现有三类解法各有边界：二阶 Taylor/Hessian 二次化需 10–30% 编码端开销且依赖高码率假设（paper:arxiv:2609.30077）；NRM 集成 + 平滑稳定化需逐 codec 线性化（paper:arxiv:2602.15779）；知识迁移（DCVC-FM→QP 图）需训练神经编码器作教师且对 HEVC 级编码器收益（8.25–8.37%）明显小于对 JM 级（20.20%），提示**编码器越强、可迁移的感知冗余越少**（paper:arxiv:2608.07799）。感知滤波器侧，非自适应通用 SR 后滤波在 RA 下色度分量恶化 +34.63%/+19.94%，内容自适应（LoRA）虽修复但引入逐序列编码端过拟合与 NNR 压缩信令链复杂度（paper:arxiv:2609.37328）。

### 3.6 信道鲁棒性与误差传播

学习式编码的熵解码在包间顺序进行，单包丢失污染后续所有包的概率估计（paper:arxiv:2609.16279）。ReLViC 以分散打包（空间相邻 token 分散至不同包）+ 双用途 Transformer（编码端熵建模/接收端恢复）联合解决，但段长参数化的依赖控制仍需在压缩效率与误差传播范围间折衷（paper:arxiv:2608.30202）；语义感知 NVC 以重要性分包 + 无包间依赖熵模型实现优雅降级，但需在抽象多级丢包信道上端到端训练，对真实无线信道模型的适配未验证（paper:arxiv:2609.16279）。质量评估侧，「可预测性异常」发现——运动不可预测内容的时域失稳不成比例地高于大幅但可预测运动内容——说明现有以空间质量为主的客观指标体系不足以刻画压缩损伤（paper:arxiv:2605.18378）。

### 3.7 码率可控性、可扩展性与评测完备性

LVC 依赖多模型/离散档位覆盖码率区间，开环 λ 接口在内容动态变化下帧级偏差累积为序列级漂移，闭环控制（PI/PID + GRU）刚起步且调节器需按 codec 训练（paper:arxiv:2604.20104）。渐进式编码的嵌入式码流推断约束（BLI 的区间收缩视角）与单模型变码率（通道掩码方案替代 40 模型）正在收敛，但两者尚未统一（paper:arxiv:2610.30966；paper:arxiv:2610.27037）。评测体系存在盲区：DCT 频谱诊断揭示标量 RD 指标掩盖 80–97% 的频谱泄漏（paper:arxiv:2611.10000）；Cheng2020-Anchor 在单频输入下产生极端钳位前输出，此类行为无法被现有基准发现（paper:arxiv:2611.10000）。实现级质量上，vvDec v3.2.1 集中修复五个安全漏洞（含 use-after-free 与堆溢出）与 SVT-AV1 v3.0.1 修复 Arm/x86 输出不一致，提示成熟开源编解码器的**平台输出等价性与内存安全仍是持续性问题**（repo_release:github:vvdec-v3.2.1；repo_release:github:SVT-AV1-v3.0.1）。

### 3.8 标准演进与神经方法的接口摩擦

AV2 以复杂度红线（编码 ≤5×、解码 ≤2×）约束工具竞赛（paper:arxiv:2605.15800），但 VVC 经验表明压缩增益与复杂度的张力只能缓解不能消除（40–50% 码率节省的代价是划分组合爆炸，paper:arxiv:2605.21526）。神经方法进入标准存在两条通道：AVS NVC 直接采纳神经 skip 模式决策进参考软件（paper:arxiv:2611.00181）、JPEG AI/IEEE 1857.11 推动学习式编码标准化（paper:arxiv:2610.22421）；但神经工具与混合框架的级联效应（修改传播至变换/量化/RDO/信令开销）、解码器可复现性约束（paper:arxiv:2609.01535）与编解码端算力不对称问题仍未有标准化的解决范式。LMCS 在 VVenC v1.14.0 中被弃用（repo_release:github:vvenc-v1.14.0）〔综述推断：反映标准工具在实测增益与实现复杂度间的动态取舍，非条目明示原因〕。

---

## 四、趋势与展望

1. **生成先验的「外挂化」与解码侧增强成为独立赛道**。Gen2-VC 证明仅训练于单一编码器的 LoRA 适配器可零重训练泛化提升 DCVC-RT/ECM/VTM/HM 的感知质量，且码流与参考帧链零改动（paper:arxiv:2609.34725）；CASR 将同一思想用于标准兼容后滤波（paper:arxiv:2609.37328）。〔综述推断〕该模式绕开了神经编码的标准化与互操作障碍，可能先于端到端神经编码器形成产业部署，但解码端 GPU/NPU 依赖与增强过程的时域稳定性（多帧独立精炼可能引入闪烁，参见 paper:arxiv:2605.18378 的时域一致性发现）是待验证问题。

2. **扩散解码从多步走向一步/少步、从头训练与零样本并行收敛**。一步去噪（YODA，paper:arxiv:2601.01141）、两步解码（DiffCR，paper:arxiv:2601.10373）、从头训练 + 蒸馏（GenVC，paper:arxiv:2607.22772）、免训练码本引导（ZeroGVC，paper:arxiv:2606.22371）与实时系统化（ReGenVC 24 fps，paper:arxiv:2607.28144）共同压缩生成式解码延迟；但当前实时性依赖 8-GPU 级算力或限定于说话人头等窄域内容，通用场景的感知-时延-算力三角仍未打破。

3. **跨平台 bit-exact 与整数化成为神经编码部署的第一性问题**。MLVC 的 Scale Sending、JOMP 的可学习混合精度整数流水线（paper:arxiv:2606.28027；paper:arxiv:2606.13110）与部署综述提出的五类系统能力框架（变率、一致性解码、鲁棒训练、渐进传输、丢包韧性，paper:arxiv:2610.22421）表明领域重心正从「RD 曲线竞争」转向「可靠可控压缩子系统」；AVS NVC 参考软件采纳 RDOSkip（paper:arxiv:2611.00181）预示神经-混合框架的标准化接口将持续细化。

4. **LLM 进入编码器设计与运维闭环**。LLM 闭环进化自动发现等价于「熵约束 RDO」的帧级 QP 启发式（三库平均省约 1.26% 码率，且经典 Lagrangian 基线反而退化 2.52–3.09%，说明朴素 λ 估计在帧级不成立）（paper:arxiv:2606.20847）；LLM 生成-评估闭环设计 Planar 预测器在 VVenC 上省 0.18% 码率（复杂度 +0.4%）并验证 ECM 集成路径（paper:arxiv:2609.01535）；边缘侧 ELLMPEG 以工具感知 RAG + 自反思本地生成 FFmpeg/VVenC 命令（78% 准确率、零 API 成本）（paper:arxiv:2602.00028）。〔综述推断〕单点增益尚小，但「LLM 作为编码工具搜索引擎」将标准开发的专家迭代范式扩展至更大设计空间，与 JVET CfE 的多档位评测要求（paper:arxiv:2605.21526）形成方法论互补。

5. **复杂度前置约束与全栈（码率-质量-解码能耗）联合优化重塑标准与流媒体工程**。AV2 将复杂度红线写入立项（paper:arxiv:2605.15800）；码率阶梯研究从 RQ 双目标扩展至码率-质量-解码时间三目标帕累托（paper:arxiv:2601.10607；paper:arxiv:2603.13597）；SVT-AV1 v4.3.0 甚至在模式决策 RD 代价中显式引入解码复杂度项（--fast-decode 3）（repo_release:github:SVT-AV1-v4.3.0）。〔综述推断〕「为低端设备设计梯子/预设」将取代纯压缩率优化成为编码工程主叙事。

6. **编码技术与 3D/生成表示的双向融合加深**。3DGS 属性经结构化排序复用标准视频编码器（paper:arxiv:2609.29041）、高斯泼溅直接作为视频压缩载体（paper:arxiv:2609.14129）、AV1 运动矢量反哺 3DGS 初始化（paper:arxiv:2605.14629）、视频编码器压缩 LLM 权重（paper:arxiv:2606.05861）表明：编码工具的输入正在从像素泛化为任意结构化张量，MPEG GS 编码标准化（ISO/IEC JTC1/SC29/WG7）将进一步牵引该方向（paper:arxiv:2609.29041）。

7. **评测体系向多维与诊断化演进**。AV2 CTC 的 6-QP 点、UGC 与自适应流配置（paper:arxiv:2605.15800）、DCT 频谱泄漏诊断（paper:arxiv:2611.10000）、时域一致性度量（paper:arxiv:2605.18378）、语义保真指标（paper:arxiv:2606.21030）与感知质量标签联合解释 64.4% MOS 方差的数据集实践（paper:arxiv:2603.26763）共同指向：**标量 RD 曲线作为唯一评价依据的时代正在结束**，频谱保真、时域稳定、语义保真与跨指标稳健性将进入常规评测协议。

---

*本综述全部结论基于给定 126 条条目；标注〔综述推断〕处为条目未直接覆盖、由综述作者基于条目内证据外推的判断。*
