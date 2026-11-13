# 视频/图像编码 · 领域综述

> 引擎合成 · 数据截止 2026-11-13 · 基于 125 条结构化条目 · glm-5.3

# 视频/图像编码领域综述

> 数据基础：截至 2026-11-13 共 125 条条目，其中 49 条版本动态覆盖 2016–2026 年主流开源编解码器（Kvazaar/dav1d/VVenC/VVDec/libavif/SVT-AV1），76 篇论文全部集中于 2026 年，后者导致研究侧视角存在时间偏置，本综述已据此控制推断范围。

---

## 一、发展历程

### 阶段一（2016–2020）：HEVC 开源编码器工程化成熟与 AV1 解码奠基

- Kvazaar v1.0.0 完成首个里程碑：全部预设经率失真-复杂度搜索重优化，veryslow 平均加速 12.42×（官方口径约 10×），相比 v0.8.3 的 3-fr 档全序列 BD-rate 降 31.0%（QP 17/22/27/32），并引入无损编码、单色、--crypto 选择性加密、--tmpv 等特性，默认启用 WPP 多线程（repo_release:github:kvazaar-v1.0.0）。
- v1.1.0 将码控下沉到 LCU 级并新增 --roi（LCU 级 delta-QP），BD 码率再降 0.5%–1.7%（repo_release:github:kvazaar-v1.1.0）；v1.2.0 全预设提速 1.19–1.28×、快速档 BD-Bitrate 最多降 14.80%，引入帧内预测模式加密与面向 360° ERP 的 --erp-aqp（repo_release:github:kvazaar-v1.2.0）。
- dav1d 0.1.0（2018-12）作为首个正式版 AV1 解码器，支持全部 AV1 特性、8–12 bit 全位深与全部色度子采样，并携带 AVX-2/SSSE3/NEON 汇编（repo_release:github:dav1d-0.1.0）。
- v1.3.0 以复杂度换效率：0-uf 档 BD-Bitrate −22.7% 但 8-vs 档速度降至 0.35×，新增 SSD 度量 CU 决策、低延迟 B 帧 GOP 与 AVX2 优化（repo_release:github:kvazaar-v1.3.0）；v2.0.0 引入 OBA 码控、VAQ 与基于机器学习的 --ml-pu-depth-intra，BD-Bitrate 较 v1.3 降 15.4%–31.1%（个别组合 hevc-D@2-vf 达 −37.4%）（repo_release:github:kvazaar-v2.0.0）。

### 阶段二（2021–2023）：VVC 软件生态起步与许可证/架构调整

- Kvazaar v2.1.0 将许可证由 LGPL2.1 改为 3-Clause BSD，并加入插值滤波器 AVX2 实现与 Y4M 输入（repo_release:github:kvazaar-v2.1.0）；v2.2.0 支持 ROI 逐帧映射、在运动搜索中更新 CABAC 上下文以提升比特代价估计精度，8-vs 档 BD-rate 降 5.6%（repo_release:github:kvazaar-v2.2.0）。
- VVDec 2.1.x 系列（2023）引入首批原生 ARM SIMD 解码优化并完成 CU=PU 结构重构与 RPL 管理重构，随后连续修复 RASL 跳过、RPR 越界读取、RPR 填充过量等缺陷（repo_release:github:vvdec-v2.1.0; repo_release:github:vvdec-v2.1.2; repo_release:github:vvdec-v2.1.3）。

### 阶段三（2024–2025）：VVC 编解码器功能补全与 AVIF HDR 生态成型

- VVDec 2.2.0 修复线程池死锁、解除 64 线程限制，并经 simd-everywhere 启用 AVX2→NEON 转译（repo_release:github:vvdec-v2.2.0）；VVenC 1.12.0 新增封顶恒定质量模式 CQF（固定 QP + QPA + 最大码率约束）与自动多线程配置，faster 档提速约 5%（repo_release:github:vvenc-v1.12.0）。
- VVDec 3.0.0 做出破坏性 API 变更（与 1.x/2.x ABI 不兼容），新增胶片颗粒支持并从 VVenC 移植 ARM SIMD（repo_release:github:vvdec-v3.0.0）；VVenC 1.12.1 将 VUI 标志对齐 DVB 规范（repo_release:github:vvenc-v1.12.1）；1.13.0 引入 ARM 优化、DASH 优化的 idr_no_radl 刷新模式与 GOP 自适应 QP 级联，medium 预设提速 5%（repo_release:github:vvenc-v1.13.0）；1.13.1 将 x86 最低指令集提升至 SSE 4.1（repo_release:github:vvenc-v1.13.1）。
- libavif 从 1.1.0 的实验性增益图与分层 AVIF（--layered，Chrome 94+ 可渐进渲染）（repo_release:github:libavif-v1.1.0），到 1.1.1 对齐 ISO 21496-1 草案（repo_release:github:libavif-v1.1.1），再到 1.2.0 正式启用增益图 API、支持 YCgCo_Re/Ro 并以 quality 系列参数取代 min/maxQuantizer（repo_release:github:libavif-v1.2.0），1.3.0 默认自动 tiling 并禁用 MC=identity+YUV400 组合以符合 AV1 规范（repo_release:github:libavif-v1.3.0）。
- Kvazaar 2.3.x 以 SIMD 优化为主（RDOQ AVX2 提速 1–3%（repo_release:github:kvazaar-v2.3.0）、帧内角度预测 AVX2 提速 1–5%（repo_release:github:kvazaar-v2.3.1)），2.3.2 修复 10-bit 与 SMP/AMP 代价计算错误后 veryslow 档较 2.3.1 BD-BR(PSNR) 降 2.7%（速度 0.77×）（repo_release:github:kvazaar-v2.3.2）；VVDec 3.1.0 新增 Loongarch 支持与 userData API（repo_release:github:vvdec-v3.1.0）。

### 阶段四（2026）：标准软件大版本连发与神经/生成式编码研究爆发

- VVenC 1.14.0 完成 NEON/SVE 大规模优化（硬件支持时默认启用 SVE），弃用 LMCS 并将 cts/dts 改为有符号整数（repo_release:github:vvenc-v1.14.0）；VVDec 3.2.0 补齐 NEON-RDM/SVE/SVE2 并引入 libfuzzer 模糊测试基础设施（repo_release:github:vvdec-v3.2.0），3.2.1 修复五个安全漏洞（含 use-after-free、堆溢出）（repo_release:github:vvdec-v3.2.1）。
- libavif 1.4.x 支持 AVIF 规范 v1.2 的 Sample Transform 与 Apple 风格增益图 JPEG，编码调优切换到 AOM_TUNE_IQ（repo_release:github:libavif-v1.4.0），1.4.1 将渐进式/分层编码转正（repo_release:github:libavif-v1.4.1）。
- SVT-AV1 在 2026-10-25 至 11-02 密集发布 9 个版本：3.1.0 新增 --rtc 模式（RTC 场景 BD-Rate 改善约 5–10%）与随机接入 S-Frame，RA 模式 M1–M5 同质量提速约 15–25%（repo_release:github:SVT-AV1-v3.1.0）；4.0.0 做破坏性 API 更新（CRF 扩展至 70、四分之一粒度步进），AVIF/静图模式提速约 5–8 倍并完成 PSY 特性向 --tune vq/iq 的移植（含 AC Bias）（repo_release:github:SVT-AV1-v4.0.0）；4.2.0 新增 TUNE-VMAF 模式（目标约 15% VMAF BD-rate 改进）、RTC CBR 码控（卡尔曼滤波 QP 估计）与 LTR 参考管理 API（repo_release:github:SVT-AV1-v4.2.0）；4.3.0 全 preset 效率再提升 5–8%，新增 --fast-decode 3（RD 代价引入解码复杂度项）与胶片颗粒 API（repo_release:github:SVT-AV1-v4.3.0）。
- 论文侧 76 篇全部出现在 2026 年，覆盖 AV2 标准工具与 CTC 评测（paper:arxiv:2601.02712; paper:arxiv:2605.15800）、学习式图像/视频压缩、生成式压缩、INR 编码、跨平台部署与编码-跨域应用，形成与工程侧并行的密集创新期。

---

## 二、技术主线与代表工作

### 主线一：混合编码标准软件的工程优化

沿「预设调优 → SIMD 纵深 → 码控/心理视觉精细化 → 场景特化」演进：Kvazaar 各版本以 BD-rate/速度的量化推进（见第一节）；SIMD 覆盖从 AVX2/SSSE3/NEON（repo_release:github:dav1d-0.1.0）扩展到 SVE/SVE2/NEON-RDM（repo_release:github:vvdec-v3.2.0）乃至 Loongarch（repo_release:github:vvdec-v3.1.0）；码控从 LCU 级（repo_release:github:kvazaar-v1.1.0）发展到 OBA/VAQ（repo_release:github:kvazaar-v2.0.0）、CQF（repo_release:github:vvenc-v1.12.0）与卡尔曼 QP 估计的 RTC CBR（repo_release:github:SVT-AV1-v4.2.0）；SVT-AV1 4.x 将心理视觉（AC Bias、variance boost）与解码复杂度感知模式决策（--fast-decode 3）纳入主线（repo_release:github:SVT-AV1-v4.0.0; repo_release:github:SVT-AV1-v4.3.0）。

### 主线二：标准编码工具设计与工具级加速

- AV2 在变换与熵编码层重设计：新增 IST、TCQ、ATC、PARA、FSC、CCTX、PH 并改进无损编码，在较低复杂度下实现显著增益（paper:arxiv:2601.02712）；AV2 CTC 实测随机访问下 AV2（v13.0）较 AV1 基准 PSNR-YUV BD-rate −29.81%、VMAF −33.79%，并新增凸包自适应流、UGC、扩展色度格式评估（paper:arxiv:2605.15800）。
- 工具级加速：FaSST 以 Givens 旋转分解替代 LFNST，RD 持平下计算量减 83.67%，最优情形 BD-rate 再省 1.80%（paper:arxiv:2605.15086）；MMVD 用 2-tap 滤波器差分将候选判决降为一次残差-梯度内积，fast 档以 −0.35% BD-rate 换 2.23% 时间节省，η 从 11.79 降至 7.10（paper:arxiv:2606.31084）；多项式图滤波器使 ECM ALF 固定滤波器数量减少一个数量级且性能相当（paper:arxiv:2607.04985）。
- 学习式工具进入标准：RDOSkip 的时域跳过决策被进行中的 AVS NVC 标准采纳并集成参考软件，AVS/HEVC 数据集分别省 0.90%/1.29% BD-rate，推理即用、无需训练（paper:arxiv:2611.00181）。

### 主线三：学习式图像压缩（LIC）

- 熵建模：HiDE 全局-局部双字典级联检索较 VTM-12.1 省 18.5%（Kodak）/24.01%（Tecnick）BD-rate（paper:arxiv:2603.06766）；ChWDTA 通道级小波域注意力八切片配置较锚点最多 −22.56%（Tecnick）（paper:arxiv:2606.00111）；ARCHE 统一分层/空间/通道先验，Kodak 上较 VVC Intra 约 −5%，参数量 95M、单图 222ms（paper:arxiv:2603.10188）；EF-LIC 以无约束向量量化+上下文自回归变换取消熵编码，编码提速 >3×、解码 >5×（paper:arxiv:2605.23323）；BLI 将渐进编码重构为区间收缩序贯推断，较 DPICT 降 17.78% BD-rate 且参数量为 CTC 的 1/5.3（paper:arxiv:2610.30966）。
- 复杂度与变码率：空间竞争多编解码器选择在 1433 MACs/像素达到 HEVC 水平（paper:arxiv:2605.13243）；通道掩码使单一 VBR 模型替代 40 个独立模型，存储缩减 14.8–15.9×（paper:arxiv:2610.27037）；训练配方上，编码器输入注入高斯噪声的噪声正则化带来跨骨干一致增益（ELIC −2.60%，DMCI-Large 相对 VTM-22.0 达 −22.02%）（paper:arxiv:2611.10073）。

### 主线四：学习式视频压缩（NVC）

Uni-LVC 以跨注意力适配与可靠性感知分类器实现单模型统一帧内/帧间、低延迟/随机访问（paper:arxiv:2603.05756）；码控方面，log 域 PI/PID + 双分支 GRU 在 DCVC 上实现 2.13% 平均码率误差与 5.69% BD-rate 改善（paper:arxiv:2604.20104）；加速与部署方面，KD-NVC 搜索-蒸馏实现 RTX 5060 上 1080p 69FPS 解码且 RD 接近 VTM-LDB（paper:arxiv:2606.04595），JOMP 混合精度整数化在 RD 对标 DCVC-FM 下位操作减 87.6%（paper:arxiv:2606.13110），MLVC 通过 Scale Sending 与 ReLU 系约束首次在 Apple/Intel/Qualcomm NPU 上 100 FPS 跑通神经视频编码，跨平台 TH XP 口径较 HEVC-QSV BD-rate −58.7%（paper:arxiv:2606.28027）；容错方面，ReLViC 以分散打包与双用途 Transformer 在严重丢包下优于 RS-FEC 保护的 H.265 与 GRACE（paper:arxiv:2608.30202）；ENVC 用事件流引导运动先验，相对 DCMVC 六基准平均 LPIPS 口径 BD-rate −67.63%（paper:arxiv:2610.02265）。

### 主线五：生成式压缩与生成先验

一步扩散方向：YODA 以时域参考多尺度特征 + 线性 DiT 一步去噪取得四个感知指标 SOTA（paper:arxiv:2601.01141）；DiffCR 两步解码相对 SOTA 扩散基线 LPIPS 口径省 27.2%、PSNR 口径省 65.1%，解码加速超 10×（paper:arxiv:2601.10373）。从零训练方向：GenVC 用自适应得分蒸馏修复 DMD 蒸馏的运动停滞，较 GLVC 匹配 LPIPS 省码率 62.5%（478M 参数、A100 上 1080p 15.1fps 单步解码）（paper:arxiv:2607.22772）。免训练方向：ZeroGVC 以码本噪声原子索引+系数引导预训练自回归视频扩散，A800 上 5–10 FPS（paper:arxiv:2606.22371）；实时方向：ReGenVC 将 77 帧说话人视频压至约 26 kB（x264/x265 需 250–280 kB），8-GPU 节点 24fps 实时、窗口延迟 972 ms（paper:arxiv:2607.28144）。生成先验复用方向：Gen2-IC 经潜空间传输桥接四个预训练生成骨干（paper:arxiv:2606.21030）；Gen2-VC 以仅训练于 DCVC-UF 的 LoRA 适配器免重训提升 DCVC-RT/ECM/VTM/HM，匹配 LPIPS 下较 VTM-23.0 平均省码率 86.65%（paper:arxiv:2609.34725）；DiV-INR 在 <0.05 bpp 极低码率相对 HEVC 取得 BD-LPIPS 0.214 的提升（paper:arxiv:2604.08329）；DCIC 以幂等约束与双衰减因子 (K_D, K_P) 实现单码流内失真-感知 Pareto 前沿连续导航（paper:arxiv:2606.13366）。

### 主线六：INR/过拟合式编码

N-O Cool-chic 用编码器网络绕过逐图过拟合，编码复杂度降低 1000 倍、解码端约 2000 次乘法/像素即达 VVC 相当性能（paper:arxiv:2607.13723）；LANCE 为 Cool-Chic 引入前向传输空间超先验实现熵模型区域自适应（Kodak 降 1.40%–2.41%）（paper:arxiv:2605.20672）；NVRC++ 将表达负担转移到高分辨率 feature grid（grid 参数 0.35M→100.06M、MAC/pixel 87.3→24.8、解码 35.5→162.9 FPS），S1–S4 四档复杂度单配置覆盖全码率区间（paper:arxiv:2606.28163）；S-NVRC 单一嵌入码流同时支持码率与解码复杂度可扩展，较 SHM-12.4 省 43.7%、较多层 VTM-20.0 省 5.6%（paper:arxiv:2609.04273）；NeR-SC 面向屏幕内容以可学习调色板与零开销帧跳过在低码率超越 H.264/H.265（paper:arxiv:2605.27024）；PIC 将静态场景短期时变重释为正向激励噪声，0.009% 压缩率实现视觉无损（DCVC-FM 需高 20.5% 码率）（paper:arxiv:2603.06095）。

### 主线七：感知/任务驱动的 RDO 与码率分配

- 指标进 RDO：LNRM 将无参考指标集成化并加梯度平滑，在 AVC 与 Cool-chic 上跨指标一致省码率且不增解码复杂度（paper:arxiv:2602.15779）；Mamba 感知损失嵌入 DCVC/HiNeRV RDO 分别省 8.46%/12.89% BD-rate（paper:arxiv:2603.25566）；IDQD 以随机 Hessian 估计二次化 FR-IQA，VVC 上五种目标度量 BD-rate 省 14.2%–36.7%（编码端开销 10–30%，解码器不变）（paper:arxiv:2609.30077）。
- 神经→传统迁移：DCVC-FM 隐式感知重要性导出块级 QP 图，不改解码语法下较 VTM-23.0 省 8.37% MS-SSIM 码率（paper:arxiv:2608.07799）；可微 H.264 代理驱动的自适应量化使语义分割任务 BD-rate 最高降 17.12%（paper:arxiv:2607.10478）。
- 面向机器：WA-RDO 以包装器感知加权 SSE 让 HEVC 级联 FCM 追平 VVC 级最优方法（paper:arxiv:2601.22070）；MT-JRD 数据集（27,264 条标注）+ AMT-JRD 预测实现三任务 BD-mAP 较 VVC +3.861%（paper:arxiv:2604.09421）；OASIS 闭环任务反馈实现 6× 压缩、链路功耗降 5.8×、任务退化 ≤1.5%（paper:arxiv:2609.15749）。

### 主线八：系统、流媒体与跨域编码

码率阶梯：JQT-PF 帕累托前沿在同 XPSNR 下较固定梯子省 11.76% 码率（激进配置 27.88%）（paper:arxiv:2601.10607），DQ-Ladder 深度强化学习阶梯较 Apple HLS 至少省 10.3% XPSNR BD-rate 且解码时间减 22%（paper:arxiv:2603.13597）；主观评测方面 LCEVC（LTM 8.1）增强层叠加 VVC 基础层的 UHD DCR 测试覆盖约 10%/50% 两个增强层码率工作点（paper:arxiv:2601.10448）；中间码方向 HLC 无数据依赖调色板在 4K@120fps 同吞吐下 LUT 资源仅为 JPEG-XS 一半、文字内容 BD-PSNR +5.312dB（paper:arxiv:2603.29864）；体积视频方向 Blackwell GPU 四路分帧 8K 10-bit 4:2:2 HEVC 达 122 fps（SFE 代价 ≤5% BD-rate）（paper:arxiv:2606.29179）；3D 资产方向复用 AV1 运动矢量使 SfM 点云密度最高 8×、3DGS 训练时间减 63%（paper:arxiv:2605.14629）、多尺度 2DGS 实现极低码率 4K 视频实时压缩（paper:arxiv:2609.14129）、双阶段 Morton 排序提升 3DGS 投影编码效率（paper:arxiv:2609.29041）；模型权重方向 LLMCodec 以仿射量化+VVC 在 LLaMA-3-8B 2-bit 下困惑度降低超 1.5 倍、下游准确率提升 21%（paper:arxiv:2606.05861）；语义通信方向 PVSC 免运动矢量传输，较 VTM+5G LDPC 基线最高省约 75%（LPIPS）/87%（DISTS）带宽且单卡 RTX 4090 实时（paper:arxiv:2605.19397）。

---

## 三、当前关键问题

### 1. 压缩效率与复杂度的剪刀差持续存在，且加速方法「寿命」短

VVC 较 HEVC 同等视觉质量省 40–50% 码率，但复杂度增长主要源自 QTMTT 划分组合爆炸；划分加速方法需随 VTM 内部启发式变化（如快速划分决策更新）持续再适配，跨多 VTM 配置与版本评估权衡本身就是挑战（paper:arxiv:2605.21526）。具体加速点的收益边界也很清晰：HFViT 帧内划分预测相对 ETH-CNN 的 VMAF BD-rate 损失改善在不同序列类间差异巨大（Class A −2.4pp vs Class E −7.9pp）（paper:arxiv:2605.29063）；MMVD 加速中经典快速算法（+Fast123）以 −0.64% BD-rate 换 21.10% 时间，而滤波器差分近似方法用 −0.35% 只换 2.23%，揭示「低损失区间内不同方法的收益曲线差异显著、需以 η 类效率-复杂度比度量」（paper:arxiv:2606.31084）。ECM 的细粒度梯度分类 ALF 滤波器数量膨胀亦需数量级压缩（paper:arxiv:2607.04985）。

### 2. 神经编解码的解码端数值确定性是部署的第一性问题

MLVC 明确定位了核心障碍：熵解码要求两端逐位一致的概率分布，而不同厂商 NPU 浮点/整数运算无法逐位复现，一个 index 错位即级联灾难性失败（DCVC-RT 在 Apple 编/Intel 解场景完全崩溃）；其 Scale Sending 将 σ 转为由 hyperlatent 显式导出（结构化共享压缩约 128×）并提供硬保证，同时以 ReLU 系激活（Apple NE 仅 ReLU/LeakyReLU 零误差）+LTR 恢复帧 + 定期 I 帧硬同步压制漂移（paper:arxiv:2606.28027）。JOMP 从训练侧构建完整整数化流水线实现确定性解码（paper:arxiv:2606.13110）；TinyLIC 部署综述将整数精度推理、跨平台一致性、变码率与标准化互操作并列为关键系统级扩展方向（paper:arxiv:2610.22421）；VQ-LIC 在 FPGA 上以 RTL 确定性周期延迟模型将部署延迟预测误差压到 0.26%/0.05%（paper:arxiv:2609.29727）。该问题尚未有跨 NVC 模型族的通用解法。

### 3. 单模型多工作点（变码率/变复杂度/多模式）仍未统一

现状是分头解决：变码率有 λ 连续控制 + log 域闭环（码率误差 2.13%–2.24%）（paper:arxiv:2604.20104）与通道掩码窄模型（替代 40 模型）（paper:arxiv:2610.27037）；变复杂度有 S-NVRC 的码率+复杂度双可扩展嵌入码流（paper:arxiv:2609.04273）与 NVRC++ 固定复杂度分档（paper:arxiv:2606.28163）；模式统一有 Uni-LVC 的帧内/帧间/低延迟/随机访问单模型（paper:arxiv:2603.05756）；质量跨度有 InnVC 单架构覆盖 >20 dB PSNR 范围（paper:arxiv:2606.13957）。但「一个模型同时覆盖全部维度」的方案在条目中不存在〔综述推断：这仍是开放组合问题〕。

### 4. 生成式压缩的可控性与可信性

- 权衡导航刚起步：DCIC 的 (K_D, K_P) 双衰减因子实现单比特流内保真-真实感连续调节，但其幂等约束只是分布感知要求的「可处理代理」而非等价物（paper:arxiv:2606.13366）。
- 动力学失真：直接 DMD 蒸馏使学生趋向运动停滞，源于学生扰动离开冻结教师训练区域后引导失效的自我强化回路，需按真值方向对齐度门控更新（paper:arxiv:2607.22772）。
- 适用域收窄：ZeroGVC 在高分辨率高码率下相对传统编码器优势收窄，作者推测 tiling 削弱了生成先验（paper:arxiv:2606.22371）；ReGenVC、DiV-INR 等的领先均限于说话人/极低码率（<0.05 bpp）等窄场景（paper:arxiv:2607.28144; paper:arxiv:2604.08329）。
- 离散化设计律尚不完整：码本容量 K 对 LPIPS 的主导性（对数线性系数 α=−0.0094，p<0.001；分辨率项不显著 p=0.68，影响比约 10×）目前仅在分层离散视频编码一个框架内成立（paper:arxiv:2607.23366）。

### 5. 指标驱动 RDO 的稳定性、指标过拟合与评测盲区

- 单指标优化会利用模型特有偏差，在其他 NRM 下收益有限甚至退化，需指标集成 + 梯度平滑（paper:arxiv:2602.15779）。
- 标量 RD 指标掩盖结构性失真：~1bpp 工作点上 BMSHJ/MBT/Cheng2020 三种 NIC 模型高频重建能量的 80–97% 泄漏到目标频带之外、目标频率增益仅 0.02–0.23；Cheng2020-Anchor 在单频输入下产生极端钳位前输出，均为标量指标不可见；仅解码器微调可将泄漏降低 90–99.8%（PSNR 代价 0.09–0.59 dB）（paper:arxiv:2611.10000）。
- 时域维度缺失：跨 AV1/HEVC/VP9/H.264 的实证显示时域一致性随码率下降非线性退化，且存在「可预测性异常」——运动不可预测内容比大幅但可预测运动内容失稳更严重，挑战以运动量定义编码难度的传统假设（paper:arxiv:2605.18378）。
- 编码器×内容交互效应显著（偏 η²=.112/.149），压缩效率结论难以跨内容条件泛化（paper:arxiv:2603.26763）。

### 6. 码率控制与自适应流的联合优化

- 两遍码控成本高：VCA 特征 + 随机森林帧级比特预测可替代 VVenC 2pRC，编码时间减 33.3%，但 B 帧预测 R² 仅 0.77（I 帧 0.93）（paper:arxiv:2602.06242）。
- 帧级 QP 决策的统计结构复杂：LLM 进化发现的「熵约束 RDO」平均省约 1.26% 码率，而经典 Lagrangian 启发式同配置反而退化（CTC B +2.68%），说明朴素 λ 估计在帧级不成立（paper:arxiv:2606.20847）。
- 阶梯优化需多目标：JQT-PF 激进配置 27.88% 码率节省以解码复杂度增加为代价，可控配置只能拿到 6.38%/6.17%（paper:arxiv:2601.10607）；码率-质量-解码复杂度三维帕累托前沿成为新基准面（paper:arxiv:2601.10607; paper:arxiv:2603.13597）。

### 7. 码流安全、鲁棒性与容错

VVDec 3.2.1 一次性修复五个安全漏洞（ALF APS use-after-free、嵌套 SEI 堆越界读+信息泄露、越界参考列表索引、SPS 整数溢出堆溢出），并强化非法码流拒绝（重叠/不完整切片覆盖、越界子图数、超 10bit 位深）（repo_release:github:vvdec-v3.2.1）；3.2.0 才引入 libfuzzer 基础设施并修复未初始化内存、负移位、整数溢出等 UB（repo_release:github:vvdec-v3.2.0）——表明成熟标准解码器的安全加固仍是持续性工程。容错侧，ReLViC 的段长参数化包上下文拓扑可在不重训练下调节压缩-误差传播权衡（paper:arxiv:2608.30202），语义/特征重要性分包 + 抗差错熵模型实现包独立解码（paper:arxiv:2609.16279），但二者均未与传统 FEC/重传机制形成统一理论。

### 8. 标准化、互操作与生态迁移成本

- API/ABI 破坏性变更频繁：VVDec 3.0.0（repo_release:github:vvdec-v3.0.0）、SVT-AV1 4.0.0（CRF 语义变更，repo_release:github:SVT-AV1-v4.0.0）、VVenC cts/dts 符号变更（repo_release:github:vvenc-v1.14.0）；工具生命周期管理出现（LMCS 弃用，repo_release:github:vvenc-v1.14.0）。
- 跨平台输出一致性本身成为缺陷类别：SVT-AV1 3.0.1 专门修复 Arm 与 x86 输出不一致（repo_release:github:SVT-AV1-v3.0.1）。
- 神经工具标准化路径初步成形但碎片化：AVS NVC 采纳学习式跳过决策（paper:arxiv:2611.00181），渐进式评测已对齐 JPEG-AI（paper:arxiv:2610.30966），增益图元数据对齐 ISO 21496-1（repo_release:github:libavif-v1.1.1）〔综述推断：学习式工具进入标准仍以「兼容现有语法的轻量插入」为主，端到端神经编码的标准化在条目中尚无进展证据〕。

---

## 四、趋势与展望

1. **生成先验的一步化与实时化**：从多步到一步/少步（YODA 线性 DiT 一步去噪 paper:arxiv:2601.01141；DiffCR 两步+10× 加速 paper:arxiv:2601.10373；GenVC 478M 参数 15.1fps paper:arxiv:2607.22772；
