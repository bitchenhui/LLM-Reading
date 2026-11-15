# 视频/图像编码 · 领域综述

> 引擎合成 · 数据截止 2026-11-15 · 基于 257 条结构化条目 · glm-5.3

# 视频/图像编码领域综述（截至 2026-11-15）

## 一、发展历程

### 1.1 HEVC/AV1 开源生态奠基与 VVC 定稿（2016–2020）

本阶段的主线是传统混合编码框架的工程成熟化。开源 HEVC 编码器 Kvazaar 于 2016-10 发布 v1.0.0：预设重优化后 veryslow 平均提速约 12.42×（官方口径约 10×），3-fr 档全序列 BD-rate 较 v0.8.3 降 31.0%，并引入无损编码、--crypto 选择性加密与 --erp-aqp 前身特性 [repo_release:github:kvazaar-v1.0.0]。随后 v1.1.0 将码控下沉到 LCU 级并新增 ROI delta-QP [repo_release:github:kvazaar-v1.1.0]；v1.2.0 全预设提速 1.19–1.28×，0-uf 档 BD-Bitrate 降 14.80%，新增帧内预测模式加密与 360° ERP 自适应 QP [repo_release:github:kvazaar-v1.2.0]；v1.3.0 以部分档位降速换取大幅压缩增益（0-uf 档 BD-Bitrate −22.7%），--rd=2 改用 SSD 度量并引入 AVX2 优化 [repo_release:github:kvazaar-v1.3.0]。AV1 侧，dav1d 0.1.0 'Gazelle'（2018-12）作为快速轻量解码器支持全部 AV1 特性与 8–12bit，在 AVX-2 平台上显著快于同期 AV1 解码器 [repo_release:github:dav1d-0.1.0]。2020 年两条标志性事件：Kvazaar v2.0.0 引入 OBA 码控与 VAQ，较 v1.3 平均 BD-Bitrate 降 15.4%–31.1% [repo_release:github:kvazaar-v2.0.0]；VVC（H.266）于 2020-07 定稿，同等主观质量下较 HEVC 约省 50% 码率 [paper:arxiv:2107.13385]。

### 1.2 VVC 工具链落地与学习式编码对标期（2021–2022）

VVC 定稿一年内，VVenC+VVdeC+FFmpeg/GPAC+DASH 构成完整开源端到端工具链，覆盖编码、封装、自适应流与播放 [paper:arxiv:2107.13385]。学习式路线此时以“辅助/混合”形态对标传统编码器：SRVC 以低分辨率码流+时变轻量超分模型流实现同等 PSNR 下 bpp 仅为 H.265 slow 模式的 16%，V100 上解码 90fps [paper:arxiv:2104.02322]；M-SRGAN 作为解码端上采样器集成进 HM 16.20，VMAF 口径 BD 码率节省 35.6% [paper:arxiv:2106.08147]；JCEVC 以压缩-增强联合优化较 x265 LDP veryfast 在 MS-SSIM 口径降 bpp 54.92% [paper:arxiv:2111.14474]。同期浮现部署侧议题：RDO-PTQ 证明以参数量化 MSE 为目标的 PTQ 对压缩任务次优，提出率失真驱动的 INT8 后训练量化 [paper:arxiv:2211.02854]；Gemino 在 Titan X 上实现 1024×1024 实时神经视频会议压缩，同感知质量下码率较传统编解码器低 2.2–5× [paper:arxiv:2209.10507]；CaDM 将降分辨率与降色深联合编码、解码端条件扩散恢复，宣称相对常见标准省 5.12–21.44× 码率 [paper:arxiv:2211.08428]。

### 1.3 LIC 越过 VVC intra 与 NVC 范式深化（2023）

2023 年学习式图像压缩（LIC）系统性超越 VVC intra：LLIC 借大核深度卷积+自适应权重在 Kodak 上较 VTM-17.0 Intra 降 BD-rate 9.49%–10.94% [paper:arxiv:2304.09571]；MLIC++ 以线性复杂度多参考熵模型在 Kodak/PSNR 口径降 13.39% [paper:arxiv:2307.15421]；频率感知 Transformer 在 Kodak/Tecnick/CLIC 上降 13.0%–15.1%（锚点 VTM-12.1）[paper:arxiv:2310.16387]；eContextformer 并行上下文模型较非并行模型解码提速约 210×、较 VTM 16.2 intra 最多省 17% 码率 [paper:arxiv:2306.14287]。视频侧，条件编码范式深化：MMVC 将块级模式决策移植到特征域 [paper:arxiv:2304.02273]、免运动两层 CANF 分层 B 帧编码节省编码端 45% MACs [paper:arxiv:2304.02690]、可训练 MCTF 小波编码 UVG 上较 HEVC 最高省 21% BD-rate [paper:arxiv:2305.16211]。标准化同步推进：JVET NNVC 参考软件 NNVC-4.0 的 NN 帧内预测与环路滤波在 RA/AI/LD 下取得 Y 分量 9.18%–11.94% BD-rate 降低 [paper:arxiv:2309.05846]。部署问题开始显性化：跨平台浮点失配由校准传输机制缓解（720p 实时解码、较 H.265 最多省 24.2%）[paper:arxiv:2309.11276]，MobileNVC 首次在移动端实时解码 1080p YUV420 [paper:arxiv:2310.01258]。方法学层面，大规模实验揭示 BD 插值误差标准场景 <0.5pp、VMAF/能耗/跨编码器场景可达 5pp，与标准化中约 1% 量级的工具采纳判据同量级 [paper:arxiv:2304.12852]。

### 1.4 全面对标 VVC 与生成式压缩爆发（2024）

DCVC-FM 将单模型 PSNR 质量范围从约 3.8 dB 扩至 11.4 dB，并在单 I 帧设置下较先前 SOTA 省 29.7% 码率、MACs 减 16% [paper:arxiv:2402.17414]；同文披露先前 SOTA 在 intra-period=−1 协议下崩塌（HEVC-E 上较 VTM +84.4%），首次系统性暴露宽松测试协议问题。RA 方向 IBVC 码率优于 VTM RA [paper:arxiv:2309.13835]。生成式压缩爆发：GLC 在 VQ-VAE 感知潜空间做变换编码，<0.04bpp 下同 FID 较 MS-ILLM 省 45% [paper:arxiv:2505.16177]（会议版为 2024）；Promptus 以提示词流替代视频流、较 H.265 省 4× 以上带宽 [paper:arxiv:2405.20032]；M3-CVC 以 LMM 层级语义+条件扩散在超低码率优于 VVC [paper:arxiv:2411.15798]。INR 路线 NVRC 在 UVG 上较 VVC VTM RA 平均增益 24% [paper:arxiv:2409.07414]。低时延基准评测显示 JVET ECM 仍综合最优（较 AVM 省 16.1%、较 DCVC-FM 省 11.0%），且神经编码器在大背景运动内容上稳定性劣于传统编码器 [paper:arxiv:2408.05042]。开源生态上 VVenC 1.12.0 引入 CQF 恒定质量模式 [repo_release:github:vvenc-v1.12.0]，VVdec 3.0.0 新增胶片颗粒支持并完成破坏性 API 变更 [repo_release:github:vvdec-v3.0.0]，Kvazaar 2.3.x 持续 AVX2 优化 [repo_release:github:kvazaar-v2.3.1]。

### 1.5 实用化拐点（2025）

DCVC-RT 实现实用化跃迁：1080p 平均 125.2fps 编码/112.8fps 解码，较 H.266/VTM 平均省 21% 码率，并指出编码速度首要瓶颈是非计算性操作（内存 I/O 与函数调用）而非计算量 [paper:arxiv:2502.20762]。GIViC 成为首个 RA 配置下超越 VTM 的 INR 编码器（YUV4:2:0、GOPSize=32 下较 VTM 省 15.94%）[paper:arxiv:2503.19604]。一步扩散压缩成型：OneDC 以单步扩散达 SOTA 感知质量，较多步扩散方案省 39% 码率、解码提速约 20× [paper:arxiv:2505.16687]；StableCodec 将可用码率下探至 0.005bpp [paper:arxiv:2506.21977]。ECVC（较 DCVC-FM 再省 10.5%/11.5%）[paper:arxiv:2410.09706]、BiECVC（RA/IP32 较 VTM 13.2 省 13.4%）[paper:arxiv:2505.09193]、DCMVC（较 VVC 省 22.7%）[paper:arxiv:2505.14541] 标志学习式编码器在各配置下全面对标或超越 VTM。JPEG AI 以主档/高档较 VVC intra 取得 13.1%/19.2% BD-rate 增益，定位首个可在移动设备部署的学习式图像编码标准 [paper:arxiv:2503.16288]。

### 1.6 部署融合与 AI 原生编码（2026）

MLVC 通过显式传输 scale 参数规避 NPU 跨平台熵解码失配，首次在 Apple/Intel/Qualcomm NPU 上跑通神经视频编码（100FPS 量级，VCD 会议基准 MOS 口径较 HEVC-QSV 的 BD-rate 提升超 70%）[paper:arxiv:2606.28027]。AV2 完成实测验证：v13.0 在 RA 配置下较 AV1 基准 PSNR-YUV 省 29.81%、VMAF 省 33.79% [paper:arxiv:2605.15800]，其变换/量化/熵编码新工具（IST、TCQ、ATC、FSC 等）构成完整技术文献 [paper:arxiv:2601.02712]。LLM 进入编码器设计闭环：闭环进化自动发现帧级 QP 启发式（三库平均约省 1.26% 码率）[paper:arxiv:2606.20847]乃至直接设计 Planar 预测器（VVenC faster 下省 0.18%）[paper:arxiv:2609.01535]。新模态持续扩展：事件引导编码 ENVC 较 DCMVC 平均省 39.13% BD-rate（PSNR-RGB）[paper:arxiv:2610.02265]、2D 高斯泼溅实现 4K 实时压缩 [paper:arxiv:2609.14129]、神经无损视频压缩 NeuralLVC 全面优于 H.264/H.265 无损模式 [paper:arxiv:2604.03353]。SVT-AV1 进入 3.x/4.x 高速迭代：3.1.0 RA 提速 15–25% 并新增 RTC 模式 [repo_release:github:SVT-AV1-v3.1.0]，4.0.0 完成破坏性 API 更新并使 AVIF 提速 5–8× [repo_release:github:SVT-AV1-v4.0.0]，4.3.0 全 preset 效率再提升 5–8% [repo_release:github:SVT-AV1-v4.3.0]。VVdec 3.2.x 补齐 ARM NEON/SVE 体系并引入 fuzzing 与五项安全修复 [repo_release:github:vvdec-v3.2.1]。

## 二、技术主线与代表工作

### 2.1 传统混合编码标准的持续演进

标准代际增益稳定在“同质量码率减半”节奏：VVC 较 HEVC 省 40–50% [paper:arxiv:2107.13385; paper:arxiv:2605.21526]，代价是编码复杂度约 10× [paper:arxiv:2312.10567]。VVC 之后的探索沿三条线：JVET ECM（2408 基准中最优）[paper:arxiv:2408.05042]、NNVC（神经网络工具进标准，NNVC-4.0 三配置 Y 分量省 9.18%–11.94%）[paper:arxiv:2309.05846]、AV2（IST/TCQ/ATC/FSC 等变换熵编码工具，实测省 29.81%–33.79%）[paper:arxiv:2601.02712; paper:arxiv:2605.15800]。传统框架内的工具级创新仍在产出：低复杂度不可分离变换 HyGT 在 HEVC 上平均省 6% 且内存较 KLT 少 6.8× [paper:arxiv:2505.21728]、INT-DTT+ 在 VVC MTS 框架下超 3% BD-rate 节省 [paper:arxiv:2511.17867]、快速二次变换 FaSST 计算量较 LFNST 降 83.67% 且 RD 持平 [paper:arxiv:2605.15086]、位置相关预测组合 PDPC 较 HEVC AI 平均省 2.0% [paper:arxiv:2505.23672]、匀加速运动模型 UAMM 与分割辅助帧间预测 SAIP 分别在 VTM 上取得 0.13% 与 0.82%（LDB 平均）增益 [paper:arxiv:2407.11541; paper:arxiv:2403.11694]。

### 2.2 学习式图像压缩：变换与熵模型的双轮演进

变换侧从 CNN/Transformer 混合（TCM）[paper:arxiv:2303.14978]、大核深卷积（LLIC）[paper:arxiv:2304.09571]、频率分解窗口注意力（FAT）[paper:arxiv:2310.16387]、窗口化通道注意力+小波下采样（SCH，四数据集较 VTM-23.1 降 18.54%–24.71%）[paper:arxiv:2409.14090]，演进到通道级小波域注意力（ChWDTA，−17.82% 至 −22.56%）[paper:arxiv:2606.00111]。熵模型侧从超先验+自回归，经棋盘/通道并行（eContextformer 解码提速 210×）[paper:arxiv:2306.14287]，到线性复杂度多参考（MLIC++）[paper:arxiv:2307.15421]、MetaFormer 式轻量变换+超先验引导全局相关（MLICv2 较 VTM-17.0 Intra 降 16.54%–24.35%）[paper:arxiv:2504.19119]、外部先验分层字典（HiDE，较 VTM-12.1 最多省 24.01%）[paper:arxiv:2603.06766]。此外出现结构化替代路线：无熵编码的 EF-LIC 用无约束 VQ+上下文条件自回归变换，编码提速 3×、解码提速 5× [paper:arxiv:2605.23323]。

### 2.3 神经视频压缩：从残差编码到条件编码再到实时化

范式主线是 DVC 系残差编码 → DCVC 系条件编码。理论侧揭示了条件编码预测路径的信息瓶颈（数据处理不等式限制预测信息传递），条件残差编码被提出以兼取两范式优势 [paper:arxiv:2307.12864]，MaskCRT 以逐像素软掩码融合两范式并在 PSNR 上匹敌 VTM-17.0 LDP [paper:arxiv:2312.15829]。上下文挖掘持续强化：结构-细节分解+长短期时域融合使学习型编解码器在全部常用数据集 PSNR/MS-SSIM 超越 VVC [paper:arxiv:2401.15864]；ECVC 引入多帧非局部相关性 [paper:arxiv:2410.09706]；BiECVC 以双向上下文门控成为首个全面超越 VTM 13.2 RA 的方案 [paper:arxiv:2505.09193]；DCMVC 以上下文补偿调制净化传播上下文 [paper:arxiv:2505.14541]。运动表示出现免运动趋势：TLZMC/IBVC 免码率插值式 MEMC [paper:arxiv:2304.02690; paper:arxiv:2309.13835]、光流增强两阶段（DCVC 上省 12.8%）[paper:arxiv:2307.05092]。统一化方面，Uni-LVC 以单模型覆盖帧内/帧间、低延迟/RA 并以可靠性门控对参考失效免疫 [paper:arxiv:2603.05756]。实时化由 DCVC-RT 标志（1080p 125.2/112.8fps）[paper:arxiv:2502.20762]，加速方法沿蒸馏搜索（KD-NVC，RTX 5060 上 1080p 69FPS）[paper:arxiv:2606.04595] 与内容自适应推理（DCVC-FM 单视频最高 41% BD-rate 提升）[paper:arxiv:2510.07283] 推进。

### 2.4 过拟合/INR 路线：解码复杂度的另一极

COIN→NeRV→HiNeRV→Cool-chic→C3 谱系以逐实例过拟合解耦泛化与容量：C3 以 <3k MACs/px 达 VTM 相当 RD [paper:arxiv:2312.02753]；Cool-chic video 仅约 800 参数、900 乘法/px [paper:arxiv:2402.03179]；缩短训练使 300 乘法/px 仍超 HEVC [paper:arxiv:2403.11651]。视频侧 HiNeRV 较 HNeRV 省 72.3% 比特率 [paper:arxiv:2306.09818]，NVRC 完成首个完全端到端 RD 优化的 INR 压缩 [paper:arxiv:2409.07414]，GIViC 首次在 RA 超越 VTM [paper:arxiv:2503.19604]，NVRC++ 以高分辨率网格+轻网络实现四档固定复杂度（7.3–357.7 kMAC/px）单配置覆盖全码率区间 [paper:arxiv:2606.28163]，S-NVRC 用单一嵌入码流同时支持码率与解码复杂度双维可扩展 [paper:arxiv:2609.04273]。编码慢的痛点由 N-O Cool-chic（编码复杂度降约 1000×）[paper:arxiv:2607.13723]、空间竞争多编解码器选择（CLIC 2020 最多省 14.5% 码率）[paper:arxiv:2605.13243]、LotteryCodec 随机子网搜索 [paper:arxiv:2507.01204] 缓解。

### 2.5 生成式与感知压缩：极低码率主战场

GAN 系（HiFiC→EGIC）之后，扩散先验成为主力：多步方案（PerCo/DiffEIC 类）感知强但解码延迟数秒；一步扩散方案 OneDC [paper:arxiv:2505.16687]、StableCodec（0.005bpp）[paper:arxiv:2506.21977]、DiffCR（两步解码、提速超 10×）[paper:arxiv:2601.10373] 解决延迟；GenVC 首个为压缩从零训练的视频扩散模型（较 GLVC LPIPS 匹配下省 62.5%，1080p 单步 15.1fps/A100）[paper:arxiv:2607.22772]；YODA 以线性 DiT 一步去噪达四项感知指标 SOTA [paper:arxiv:2601.01141]；ZeroGVC 实现免训练低延迟生成式压缩（A800 上 5–10FPS）[paper:arxiv:2606.22371]。RDP 权衡的可操作性由 DCIC 的双衰减因子单码流 Pareto 调节提供 [paper:arxiv:2606.13366]。垂直域超低码率（<0.05bpp）人脸/说话人视频：PFVC [paper:arxiv:2410.08485]、ReGenVC（77 帧约 26kB、8-GPU 24fps 实时）[paper:arxiv:2607.28144]。生成先验与传输表示解耦的 Gen2-VC 以解码侧 LoRA 适配器在码流零改动下匹配 LPIPS 较 VTM-23.0 省 86.65% [paper:arxiv:2609.34725]。感知失真建模本身也在演进：Wasserstein 失真使 C3 以不到 HiFiC 1% 的解码计算量达到相当感知质量-码率权衡 [paper:arxiv:2412.00505]。

### 2.6 面向机器的编码（ICM/VCM）

MPEG VCM 双轨推进：特征压缩端到端多尺度模型较先前方法至少降 52% BD-rate、编码时间较 VVC 基方案减 5–27× [paper:arxiv:2306.16670]；TransVFC 的“压缩后转移”范式以轻量 FST 模块适配新任务而无需重训编解码器 [paper:arxiv:2603.23772]。任务迁移由 TransTIC 的提示机制 [paper:arxiv:2306.05085] 发展到 MoECodec 的 token 级 MoE 路由（分类/检测/分割 BD-rate 分别 −7.74%/−8.98%/−9.72%，远优于 adaptation 基线）[paper:arxiv:2606.21033]。恰可识别差异（JRD）建模从单任务 DT-JRD（较 VVC 省 29.58% 且保检测精度）[paper:arxiv:2411.09308] 走向多任务 MT-JRD（27,264 条标注+属性辅助预测，BD-mAP 较 VVC +3.861%）[paper:arxiv:2604.09421]。率分配层面，MFIBA 以多尺度特征重要性在检测任务较 ELIC 锚点省 38.202% [paper:arxiv:2503.19278]。面向 LVLM 的通用语义压缩将优化目标从任务级损失改为语义 token 损失，率-准确率显著优于 VVC [paper:arxiv:2407.17060]。

### 2.7 编码器智能加速与学习增强

VVC QTMTT 划分搜索是复杂度主源（64×64 intra CTU 最坏情形约 2000× HEVC 块数）[paper:arxiv:2605.21526]。加速路线从轻量 CNN 划分深度预测（VTM10 RA 提速 17–30%、BD-rate +0.37–1.18%）[paper:arxiv:2312.10567]、划分图方法（RA 省 51.30% 编码时间、BDBR 2.12%）[paper:arxiv:2504.18398] 到 CPU 友好的 CNN-Transformer 混合 HFViT [paper:arxiv:2605.29063]。工具级加速：2-tap 滤波器差分将 VVenC MMVD 候选判决降为一次内积，fast preset 下 BD-rate −0.35% 即拿走大部分加速收益 [paper:arxiv:2606.31084]。码控加速：低复杂度第一遍降 VVenC 全帧内编码时间 32%（BD-rate +2%）[paper:arxiv:2306.16786]、VCA 特征+随机森林降 33.3% [paper:arxiv:2602.06242]。神经网络工具低复杂度化：LUT 化 NN 环路滤波以 0.10–0.51% BD-rate 增益、约翻倍时间开销实现部署 [paper:arxiv:2407.10926]。感知 RDO：IDQD 以 Hessian 二次化将 FR-IQA 引入块级 RDO（五种度量 BD-rate 省 14.2–36.7%）[paper:arxiv:2609.30077]；NRM 集成优化适配 UGC [paper:arxiv:2602.15779]；码率分配迁移把 DCVC-FM 的感知重要性蒸馏为传统编码器 QP 图（较 HM-16.20 省 8.25%）[paper:arxiv:2608.07799]；H.264 可微代理驱动自适应量化（分割 BD-rate −17.12%）[paper:arxiv:2607.10478]。

### 2.8 系统、传输与部署

跨平台一致性：从校准流 [paper:arxiv:2309.11276]、SSF 超先验静态量化（同机 BD-rate 代价 +9.02%–9.93%）[paper:arxiv:2410.20145]，到 DCVC-RT 模型整数化 [paper:arxiv:2502.20762]、JOMP 混合精度量化（位操作减 87.6%）[paper:arxiv:2606.13110]、MLVC scale 显式传输 [paper:arxiv:2606.28027]。端侧轻量：MCUCoder 以 10.5K 参数适配 1–2MB RAM MCU，较 M-JPEG 省约 55% [paper:arxiv:2411.19442]；FPGA 上 VQ-LIC 在 220-DSP Zynq-7020 达 47.98fps [paper:arxiv:2609.29727]。硬件评估：软件解码甜点为 AV1（较 VP9 能耗仅 +16.55%、省 43.95% 码率），硬件解码甜点为 HEVC，硬件解码器能耗不足优化软件的 9% [paper:arxiv:2402.09001]；GPU 硬件编码器实时 RD 可匹敌软件编码器但代际 RD 提升甚微 [paper:arxiv:2511.18686]。流媒体系统：帕累托前沿码率阶梯（同 XPSNR 省 11.76%）[paper:arxiv:2601.10607]、DRL 码率阶梯 DQ-Ladder（较 HLS 至少 −10.3% 且解码时间 −22%）[paper:arxiv:2603.13597]、LCEVC 增强层主观评估 [paper:arxiv:2601.10448]。抗丢包与信道：GRACE 联合训练抗丢包（不可解码帧 −95%、卡顿 −90%）[paper:arxiv:2305.12333]、ReLViC 分散打包+双用途 Transformer [paper:arxiv:2608.30202]、语义感知抗差错 NVC [paper:arxiv:2609.16279]、语义通信/JSCC（PVSC 较 VTM+5G LDPC 省 75–87% 带宽）[paper:arxiv:2605.19397]。

### 2.9 评测方法学、数据集与标准化

评测维度扩展：BD 教程综述与误差分析 [paper:arxiv:2304.12852; paper:arxiv:2401.04039]、会议场景 VCD [paper:arxiv:2309.07376]、训练集 BVI-AOM（956 序列）[paper:arxiv:2408.05042]、通用基准 USTC-TD [paper:arxiv:2409.08481]、屏幕内容 SDU-SCICD10K [paper:arxiv:2502.15174]、相机原生谈话头数据集（838 段 FFV1，H.266 较 H.264 VMAF BD-rate 最高 −71.3%）[paper:arxiv:2603.26763]、DCT 频谱诊断（发现 NIC 高频能量 80–97% 泄漏到目标频带外）[paper:arxiv:2611.10000]、时域一致性实证 [paper:arxiv:2605.18378]。标准化：JPEG AI（ISO/IEC 6048/ITU-T T.840，含变码率机制至 2.0bpp）[paper:arxiv:2503.16288; paper:arxiv:2510.13867]、IEEE 1857.11 采纳 iWaveV3 为候选 [paper:arxiv:2403.05937]、AVS NVC 参考软件集成 RDO 优化的跳过模式 [paper:arxiv:2611.00181]、MPEG GS 编码 CTC 启动（双阶段 Morton 排序方案为代表）[paper:arxiv:2609.29041]。

## 三、当前关键问题

### 3.1 复杂度墙：编码侧与解码侧的不对称困境

传统侧，VVC 编码复杂度约为 HEVC 的 10×，QTMTT 划分搜索为最大来源 [paper:arxiv:2312.10567]，这使加速方法必须随 VTM 内部启发式演进持续适配——在旧 VTM 上报告的“−50% 时间”可能被“新版 VTM+调低 MTT 深度”这一零成本操作吞没 [paper:arxiv:2605.21526]。神经侧，自编码器 LIC 解码复杂度可达每像素 10⁵–10⁶ 次乘法量级，移动端不可部署 [paper:arxiv:2307.12706]。DCVC-RT 的关键诊断是：编码速度的首要瓶颈是非计算性操作（内存 I/O 开销 Psize 与函数调用开销 Pnum），而非多数工作关注的 MACs——这解释了“通道减半、算力平方下降但时间近似线性改善”的现象，也意味着单纯算力量化指标（FLOPs/MACs）不足以排序神经压缩方法 [paper:arxiv:2502.20762; paper:arxiv:2311.12821]。率-失真-计算三维评测开始被明确提出 [paper:arxiv:2311.12821]，按每像素 MACs 归一化的 RD 基准（如 ShiftLIC 的 −102.6%）成为新口径 [paper:arxiv:2503.23772]。高分辨率下实时解码仍是硬约束：DCVC-HEM 在 UVG 4K 上实测仅 0.53FPS [paper:arxiv:2609.14129]。

### 3.2 跨平台数值一致性与整数化

神经编码器的熵编码要求编解码两端概率分布逐位一致，而不同厂商 NPU 即便同为 FP16/INT8 也无法逐位复现，一个 index 错位即级联成灾难性解码失败 [paper:arxiv:2606.28027]。解决谱系：(1) 校准辅助码流——编码端识别可能跨量化边界的熵参数并显式传输坐标 [paper:arxiv:2309.11276]，但只是概率性缓解 [paper:arxiv:2606.28027]；(2) 全整数化——DCVC-RT 采用 W16A16 [paper:arxiv:2502.20762]，JOMP 将量化步长与位宽同时作为可学习变量做混合精度（位操作 −87.6%，RD 对标 DCVC-FM）[paper:arxiv:2606.13110]；(3) 结构性改造——MLVC 将 scale 参数从隐式推断改为经固定 factorized 熵编码显式导出，从机制上消除失配 [paper:arxiv:2606.28027]。任务导向 PTQ（RDO-PTQ）同样以率失真损失而非参数 MSE 为目标 [paper:arxiv:2211.02854]。该问题已成为神经编码进入产品系统的先决条件 [paper:arxiv:2610.22421]。

### 3.3 单模型宽质量范围、变码率与码控闭环

传统编码器天然支持连续 QP 调节，而神经编码器长期绑定固定 λ 训练多套模型。DCVC-FM 通过可学习量化缩放+均匀量化参数采样将单模型 PSNR 范围从 3.8dB 扩至 11.4dB [paper:arxiv:2402.17414]；JPEG AI 标准化将变码率作为核心特性（连续码率函数至 2.0bpp）[paper:arxiv:2503.16288]；通道级掩码引导方法以单一 VBR 模型替代 40 个独立模型、存储缩减 14.8–15.9× [paper:arxiv:2610.27037]；渐进式编码走向区间收缩下的序贯隐变量推断（BLI 较 DPICT 降 17.78%）[paper:arxiv:2610.30966]。但码率“可达”不等于“分配最优”：开环 λ 接口在内容动态变化下序列级码率漂移，需 log 域 PI/PID 闭环+GRU 调节器实现精准跟踪（平均码率误差 2.13%–2.88%，BD-rate 再降 4.49%–5.69%）[paper:arxiv:2604.20104]。

### 3.4 长预测链误差累积与测试协议失真

DCVC-FM 首次系统性披露：先前 SOTA（DCVC-DC）在 CTC 规定的 intra-period=−1（全序列单 I 帧）下性能崩塌，HEVC-E 上较 VTM 码率 +84.4%——此前“超越传统 codec”的结论部分建立在小 intra-period 宽松协议上 [paper:arxiv:2402.17414]。缓解机制包括周期性上下文刷新 [paper:arxiv:2402.17414]、上下文补偿调制 [paper:arxiv:2505.14541]、部分级联微调抑制训练-测试序列长度失配 [paper:arxiv:2410.09706]、BiECVC 的数据依赖衰减启发双向门控 [paper:arxiv:2505.09193]。协议反思延伸到基准评测：低时延配置的系统性对比长期缺失，且神经编码器在大背景运动内容上表现出不一致性能 [paper:arxiv:2408.05042]。

### 3.5 条件编码的信息瓶颈与解码端状态开销

条件编码虽理论熵界不高于残差编码，但预测路径受数据处理不等式约束、网络容量有限，极端情形（x_t≡x_c）下无法零码率完美重建 [paper:arxiv:2307.12864]。DCVC 系以缓存大量传播特征缓解，代价是巨大解码图像缓冲：DCVC-TCM/HEM/DC 需 67/67.75/55.75 张全分辨率特征图当量，高分辨率高帧率下片外访存带宽问题长期被忽视 [paper:arxiv:2312.15829]。缓解路线：MaskCRT 软掩码混合两范式 [paper:arxiv:2312.15829]、HyTIP 混合显式解码帧+少量隐特征的递归传播 [paper:arxiv:2508.02072]、MH-LVC 限制每次预测最多两个参考帧 [paper:arxiv:2510.12479]、NVRC++ 将表达负担从网络卸载到高分辨率网格（解码 162.9FPS）[paper:arxiv:2606.28163]。

### 3.6 感知-失真-真实感三角与生成式压缩的落地障碍

RDP 理论约束下，生成式压缩面临三重落地问题。其一，解码延迟：多步扩散方案单图解码数秒（PerCo 3.742s、DiffEIC 7.423s 量级）[paper:arxiv:2506.21977]、生成式视频编码长期无实时方案 [paper:arxiv:2607.28144]；一步扩散已证明“多步采样并非必需” [paper:arxiv:2505.16687]，ZeroGVC/ReGenVC 将帧率推至 5–24FPS 量级 [paper:arxiv:2606.22371; paper:arxiv:2607.28144]，但距通用实时仍有距离。其二，保真与幻觉：扩散采样不保证像素级一致，语义漂移（文字损坏、人脸身份变化）在监控等强保真场景不可接受 [paper:arxiv:2603.06095; paper:arxiv:2606.21030]；单码流内连续调节保真-真实感权衡（DCIC 双衰减因子）成为可操作化方向 [paper:arxiv:2606.13366]。其三，UGC 非纯净参考：保真驱动 RDO 会复刻甚至强化源中已有伪影，需将参考从像素锚点降格为上下文引导（Mamba 感知损失在 DCVC/HiNeRV 上分别省 8.46%/12.89%）[paper:arxiv:2603.25566]。此外生成先验与编解码器的解耦复用（Gen2-VC 的 LoRA 适配器跨 DCVC-RT/ECM/VTM/HM 泛化）是降低该路线边际成本的关键 [paper:arxiv:2609.34725]。

### 3.7 面向机器的编码：表示选择、任务泛化与机器感知阈值

核心张力在“传像素还是传特征”：特征压缩码率低、可隐私保护，但重构特征只适配有限任务网络、泛化性差 [paper:arxiv:2407.17060]。多任务与人机联合感知的方案尚在收敛：单流压缩域表示（JPEG AI 定位）[paper:arxiv:2510.13867]、token 级动态算力分配（MoECodec）[paper:arxiv:2606.21033]、压缩后转移（TransVFC）[paper:arxiv:2603.23772]。级联管线中内层编码器的 SSE-RDO 与后处理包装器失配导致比特浪费，包装器感知 RDO（WA-RDO）可使 HEVC 级联追平 VVC 级最优 [paper:arxiv:2601.22070]。机器侧 JND（JRD）的预测建模刚从单任务走向多任务（MAE 3.781）[paper:arxiv:2604.09421]，与感知编码成熟的 JND 体系相比仍处早期。

### 3.8 评测方法学：从标量 RD 到多维保真

四个具体缺口：(1) BD 插值误差在 VMAF/能耗/跨编码器场景可达 5pp，与 1% 量级工具采纳判据同量级，且各开源实现的拟合器/对数底不统一 [paper:arxiv:2304.12852; paper:arxiv:2401.04039]；(2) 数据集与部署场景错位——高制作水准基准主导评测，会议 [paper:arxiv:2309.07376]、UGC [paper:arxiv:2605.15800]、屏幕内容 [paper:arxiv:2502.15174]、谈话头 [paper:arxiv:2603.26763] 等场景统计特性系统性不同，且编码器×数据集交互效应显著；(3) 标量 RD 掩盖结构性失真——NIC 在 ~1bpp 工作点高频重建能量 80–97% 泄漏到目标频带外、目标频率增益仅 0.02–0.23 [paper:arxiv:2611.10000]，时域一致性随压缩非线性退化且运动可预测性比运动量更决定失稳 [paper:arxiv:2605.18378]；(4) 率-失真-计算联合口径尚未标准化，FLOPs 与运行时均不足以单独排序方法 [paper:arxiv:2311.12821]。

### 3.9 传输鲁棒性与跨层联合优化

严格时延约束下重传不可行，帧内丢包率可能远超网络丢包率 [paper:arxiv:2305.12333]。学习式编码的结构化隐表示对突发丢包更脆弱：连续段打包会产生隐域大块连续缺失，且包间熵依赖导致误差级联 [paper:arxiv:2608.30202]。方向包括编解码联合丢包训练（GRACE）[paper:arxiv:2305.12333]、分散打包+双用途 Transformer 恢复（ReLViC）[paper:arxiv:2608.30202]、语义重要性分包与抗差错熵模型 [paper:arxiv:2609.16279]、语义通信/JSCC 端到端设计（PVSC 单卡 RTX 4090 实时）[paper:arxiv:2605.19397]。分离式“VTM+5G LDPC”基线在低 SNR 短块长场景的失配被量化 [paper:arxiv:2605.19397]，但语义通信的编解码生态、边信息格式与参考缓冲标准化仍是空白 [paper:arxiv:2605.19397]。

## 四、趋势与展望

**（1）标准化与学习式方法的融合加速。** JPEG AI 已作为 ISO/IEC 6048/ITU-T T.840 发布并定位首个移动端可部署的学习式图像标准 [paper:arxiv:2503.16288; paper:arxiv:2610.22421]；NNVC 验证了 NN 工具进 JVET 标准的可行路径 [paper:arxiv:2309.05846]；AVS NVC 参考软件已集成学习式跳过模式决策 [paper:arxiv:2611.00181]。〔综述推断〕下一代标准（VVC 之后的 JVET 主线）将大概率采取“传统工具+选择性 NN 工具”的混合形态，且 NN 工具的采纳判据会附加复杂度与一致性硬约束——AV2 已把编码复杂度 ≤5× AV1、解码 ≤2× 前置为红线 [paper:arxiv:2605.15800]，这一做法将成为后续标准制定的范式。

**（2）实用化主线从“超越 VTM”转向“可部署地超越”。** DCVC-RT、MLVC、KD-NVC、JOMP 等工作表明研究重心已移向实时吞吐、整数化一致性、码控与 NPU 兼容 [paper:arxiv:2502.20762; paper:arxiv:2606.28027; paper:arxiv:2606.04595; paper:arxiv:2606.13110]。部署导向综述与开放基准（TinyLIC：10 kMACs/px 超 HEVC、50 kMACs/px 匹配 VVC）正在把变码率、整数推理、鲁棒性、互操作确立为系统级评测维度 [paper:arxiv:2610.22421]。〔综述推断〕神经编码器在视频会议等特定垂类（MLVC 在 VCD 上 MOS 口径较 HEVC-QSV 提升超 70% [paper:arxiv:2606.28027]）将率先商用，通用分发场景仍将长期由 AV1/AV2/VVC 硬件生态主导——硬件解码能耗不足优化软件的 9% [paper:arxiv:2402.09001] 且 GPU 硬件编码 RD 已可匹敌软件 [paper:arxiv:2511.18686]。

**（3）生成先验作为“解码侧外挂”的解耦架构。** Gen2-VC 证明轻量 LoRA 适配器可在码流与参考帧链零改动下复用于多个异构编码器 [paper:arxiv:2609.34725]；一步扩散持续压缩解码延迟 [paper:arxiv:2505.16687; paper:arxiv:2601.10373]。〔综述推断〕“标准码流+解码侧可插拔生成增强”将成为感知质量升级与标准演进解耦的产业路径，其标准化形态（模型信令、NNR 类压缩 [paper:arxiv:2609.37328]、向后兼容）是关键待解问题。

**（4）LLM/自动化方法进入编码器开发闭环。** 已验证范围从命令生成（ELLMPEG，78% 准确率、零 API 成本）[paper:arxiv:2602.00028]、帧级 QP 启发式进化（平均省 1.26%）[paper:arxiv:2606.20847] 推进到编码工具本体设计（Planar 预测器，0.18%）[paper:arxiv:2609.01535]。〔综述推断〕随着闭环评测成本下降，LLM 驱动的工具提案-验证将补充乃至部分替代标准化中的专家提案流程，但语法信令与解码端可复现性约束仍是主要瓶颈 [paper:arxiv:2609.01535]。

**（5）模态与对象扩展。** 视频编码技术正在外溢：事件相机引导编码 [paper:arxiv:2610.02265]、3DGS/点云编码进入 MPEG GS 标准化 [paper:arxiv:2609.29041]、高斯泼溅作为视频表示（GSVC 1080p 1500fps 渲染）[paper:arxiv:2501.12060; paper:arxiv:2609.14129]、视频编解码器用于 LLM 权重压缩 [paper:arxiv:2606.05861]、神经无损视频压缩 [paper:arxiv:2604.03353]、传感器内闭环压缩（OASIS，6× 压缩、功耗降 5.8×）[paper:arxiv:2609.15749]。VVC 硬件编码支撑 8K 10-bit 4:2:2 V-PCC 实时流（122fps）[paper:arxiv:2606.29179] 显示传统标准向体积视频等新负载延伸。

**（6）评测体系的多维化。** 复杂度约束前置进入 CTC（AV2 案例）[paper:arxiv:2605.15800]、UGC/AS 凸包/扩展色度纳入正式评测 [paper:arxiv:2605.15800]、频谱保真与时域一致性等结构化诊断补位 [paper:arxiv:2611.10000; paper:arxiv:2605.18378]、训练数据工程化（BVI-AOM 许可松绑）[paper:arxiv:2408.05042]。〔综述推断〕“率-失真-计算-鲁棒-任务”五维权衡将取代单一 RD 曲线成为领域默认报告口径，跨平台一致性与解码能耗有望进入标准化符合性测试。

**总体判断**：截至 2026-11，该领域正处于三线交汇期——传统标准线（AV2/ECM/NNVC）以复杂度为约束持续收割工具红利；神经编码线在 RD 越过 VTM 后把主战场转向部署属性（实时、一致、可控、鲁棒）；生成式线在极低码率感知质量上打开传统框架不可达的空间，其与传输表示的解耦正使“标准码流+智能增强”的分层生态成为可能。三线之间的方法互鉴（传统 RDO 思想回流神经编码 [paper:arxiv:2611.00181]、神经工具进入标准 [paper:arxiv:2309.05846]、感知度量驱动传统编码器 [paper:arxiv:2609.30077]）将是未来数年最富产出的方向。
