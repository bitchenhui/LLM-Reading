# PSNR · 实体档案

> metric:PSNR · 数据截止 2026-11-16 · 关联 97 条 · glm-5.3

# 实体档案：PSNR（metric:PSNR）

## 档案概览

| 字段 | 内容 |
|---|---|
| 实体 ID | metric:PSNR |
| 类型 | metric（质量度量） |
| 名称 | PSNR |
| 方向 | 越高越好 |
| 挂接条目 | 97 条（本卷收录时间跨度 2017-11-17 → 2026-11-11） |
| 条目构成 | 论文为主（约 60+ 条），版本发布 5 条（Kvazaar ×2、libavif、SVT-AV1 ×2），标准化提案 2 条（JVET） |
| 度量属性 | 全参考（full-reference）像素级保真指标——退化分类框架将其归入全参考 IQA 指标（paper:arxiv:2605.15906），并与 MSE/SSIM 并列称“像素级指标”（paper:arxiv:2608.24782）。注册表未登记计算式，档案仅基于用法侧刻画 |

**用法谱系（基于挂接条目归纳）**：
1. **绝对 dB 值**：重建/超分质量报告（如 HST 23.51 dB，paper:arxiv:2208.09885）；
2. **dB 增量**：修复/增强类工作的头号卖点数字（+0.14 dB 至 +8.35 dB 均有出现）；
3. **BD-PSNR / BD-rate(PSNR)**：编解码器与压缩方案对比的标准口径（Bjøntegaard 体系，见下文）；
4. **挑战赛评分轴**：NTIRE 2021 Track 1/3 以 PSNR 定保真、Track 2 转感知质量（paper:arxiv:2104.10781）；
5. **质量范围规格**：以单模型覆盖的 PSNR 区间刻画编码器宽质量能力（paper:arxiv:2402.17414、paper:arxiv:2606.13957）；
6. **被预测目标**：无参考 PSNR 估计（paper:arxiv:2607.27628、paper:arxiv:2607.23321）。

---

## 关键事实与演进

### 2017–2020：编解码器版本节点中的奠基用法
- Kvazaar v1.2.0 以 BD-Bitrate（PSNR 族 RD 口径）量化快速预设压缩效率改善（0-uf 档总体降 14.80%，hevc-B 0-uf 降 19.04%）（repo_release:github:kvazaar-v1.2.0）——确立开源编码器发布说明以 PSNR 口径 RD 数据自证的惯例，延续至今（repo_release:github:kvazaar-v2.3.2）。

### 2021：超分/修复领域成为 PSNR 增量的高产区
- NTIRE 2021 压缩视频质量增强挑战赛明确分轨：Track 1/3 以 PSNR 提升保真度，Track 2 以感知质量为目标——同一赛事内 PSNR 与感知指标的分野首次被制度化（paper:arxiv:2104.10781）。
- dB 增量密集报告：BasicVSR++ 相近参数量下 +0.82 dB（vs BasicVSR）（paper:arxiv:2104.13371）；meta-attention 通用 SR 模型平均 +0.2969 dB、人脸 SR +0.3320 dB（模糊/降采样 X4）（paper:arxiv:2110.14638）；T-tetromino+LFCR 相对 VDSR 最高 +1.92 dB（paper:arxiv:2111.09013）。
- “等 PSNR 码率比较”范式成型：SRVC 达相同 PSNR 时 bpp 仅为 H.265 slow 的 16%、DVC 的 2%（paper:arxiv:2104.02322）；JCEVC 同 PSNR 下较 x265 LDP very fast 降 bpp 39.39%（paper:arxiv:2111.14474）。光场编码侧出现 BD-PSNR=1.35 dB 的 SOTA 声明（摘要自报）（paper:arxiv:2103.04201）。

### 2022：量化与复合退化场景下的 PSNR 追踪
- 超低比特量化线：DDTB 将 EDSR 量化至 2 bit（x4）在 Urban100 上 +0.70 dB（paper:arxiv:2203.03844）；QuantNAS 以 PSNR/BitOps 权衡为搜索目标（paper:arxiv:2208.14839）。
- 压缩图像超分以绝对 PSNR 记录挑战赛成绩（HST 23.51 dB，AIM 2022 赛道第五）（paper:arxiv:2208.09885）。

### 2023：方法论审视与域外扩张
- **BD 方法论奠基性审计**：大规模实验表明 BD 计算在 PSNR 率失真比较的标准应用中最准确（平均插值误差 <0.5 pp），VMAF/能耗/跨编解码器等非标准场景最大可达 5 pp，增加 QP 支撑点可使误差约减半（paper:arxiv:2304.12852）。
- **标准化域扩张**：JVET 两度提案（2023-01、2023-07）为 V3C V-PCC 点云评估引入“仅占用率 PSNR”计算方法（standard_proposal:jvet:m193-AC0044、standard_proposal:jvet:m195-AE0092）；LiDAR 点云压缩采用点对点 PSNR 口径（SCP 最高省 29.14% BD-Rate）（paper:arxiv:2308.12535）；G-PCC 属性增强报告 Y/Cb/Cr 分量 BD-PSNR +0.43/+0.25/+0.36 dB（稠密点云）（paper:arxiv:2303.13764）。
- 学习式编解码以 PSNR BD-rate 对标 VTM 成为常规：MLIC++ 在 Kodak 上相对 VTM-17.0 降 13.39%（paper:arxiv:2307.15421）；ConvNeXt-ChARM 四数据集平均 −5.24%（paper:arxiv:2307.06342）；INR 线 HiNeRV 在 UVG（PSNR 口径）较 HNeRV 省 72.3%（paper:arxiv:2306.09818）。

### 2024：基准体系化与质量范围叙事
- BD 综述确认其 2001 年 VCEG-M33 起源即以 PSNR 为失真指标，后续扩展至 SSIM/VMAF/MOS 但易被误读（paper:arxiv:2401.04039）。
- 跨阵营低时延基准以 PSNR BD-rate 定胜负：ECM 相对 AVM 省 16.1%、相对 DCVC-FM 省 11.0%（paper:arxiv:2408.05042）。
- 质量范围规格化：DCVC-FM 单模型 PSNR 范围从先前同类约 3.8 dB 扩至约 11.4 dB（paper:arxiv:2402.17414）。
- 域变体：360° 视频采用 WS-PSNR，ACP/ECP 投影对最新一代 NVC 相对 ERP 码率节省 >55%（paper:arxiv:2402.10257）；流媒体凸包实测 PSNR 工作区间 20–40 dB（paper:arxiv:2408.09044）。
- 数据集以 PSNR 增益自证价值：BVI-AOM 训练集带来 PSNR-Y 口径最高 0.29 个百分点码率节省（paper:arxiv:2408.03265）；USTC-TD 以 PSNR/MS-SSIM/VMAF/MOS 建立基准（paper:arxiv:2409.08481）。
- 大幅 dB 增量案例：2DQuant 2 bit 下 Set5(x2) 较 SOTA +4.52 dB（paper:arxiv:2406.06649）；实例自适应微调 RD 曲线最高提升约 5 dB（paper:arxiv:2405.08530）；NVRC 相对 VVC VTM RA 平均 24% 编码增益（UVG、PSNR 口径）（paper:arxiv:2409.07414）。

### 2025：主观效度验证与增强后处理量化
- **关键效度证据**：216 条 4K 序列、30 人受控主观实验表明，VMAF 等主流指标对神经编解码器仍有效，传统与神经编解码器间无显著差异；**PSNR 在跨编解码器的序列内比较中 Spearman 秩相关最高**（paper:arxiv:2511.00969）。
- 解码端质量增强以 PSNR 结算：OVQE-VVC 平均 +0.74 dB、最高 1.2 dB，等效省码率约 19.6%（paper:arxiv:2504.19935）。
- Kvazaar v2.3.2：veryslow 预设 v2.3.2 对比 v2.3.1 整体 BD-BR(PSNR) 降 2.7%、BD-BR(SSIM) 降 3.0%，速度 0.77×（repo_release:github:kvazaar-v2.3.2）。
- JPEG AI 标准将 PSNR-HVS 列入七项质量指标族（与 MS-SSIM、VMAF 等并列）报告相对现有标准的 BD-rate 降低（paper:arxiv:2510.13867）。
- INR/网格路线持续以 PSNR 口径刷新：NVTM 相对以往网格类方法 UVG(Dynamic) 平均 +1.54 dB（paper:arxiv:2505.00335）；NVRC-Lite 相对 C3 最多省 21.03% BD-rate（PSNR 口径）（paper:arxiv:2512.04019）。

### 2026：变体增殖、盲预测与批判性反思并行
- **标准侧**：AV2 CTC 实测 AV2 v13.0 相对 AV1 在随机访问下 PSNR-YUV 口径省 29.81% BD-rate（VMAF 口径 33.79%）（paper:arxiv:2605.15800）；SVT-AV1 v4.2.0 新增 TUNE-VMAF 模式，目标约 15% VMAF BD-rate 改进而“PSNR 损失极小”——编码器调优中 PSNR 与感知指标被显式作为可交换的权衡轴（repo_release:github:SVT-AV1-v4.2.0）；v4.0.0 在 tune MS-SSIM 下同质量提速 5–8 倍（repo_release:github:SVT-AV1-v4.0.0）；libavif v1.4.0 发布（挂接上下文为 AVIF 编码调优演进）（repo_release:github:libavif-v1.4.0）。
- **变体与后继**：SI-PSNR（锐度感知）在 IQA 基准上的相关性统计优于所有其他 PSNR 变体，且锐度感知损失恢复的图像获 67% 二值主观偏好（paper:arxiv:2608.13989）；VVC 流媒体码率梯子优化改用 XPSNR 为质量锚（同 XPSNR 下 JQT-PF 省 11.76% 码率）（paper:arxiv:2601.10607）。
- **盲预测成熟**：BlindPSNR 无参考预测 PSNR，将低照度增强 top-1 参数选择精度从 54.4% 提至 89.5%、选择遗憾从 1.62 dB 降至 0.026 dB；七个 NR-IQA 基线 top-1 精度均为 0%（面向感知而非信号保真）（paper:arxiv:2607.27628）；ISP 评估以代理参考图无参考估计 PSNR/SSIM/LPIPS（paper:arxiv:2607.23321）。
- **适用边界被逐域标定**：超透镜域 PSNR 与人类语义可解读性一致性有限（paper:arxiv:2605.29212）；胸片场景 SSIM/PSNR 常与专家诊断可用性判断不一致（paper:arxiv:2607.26333）；海事能见度场景 PSNR 无法建立物理可解释关系（paper:arxiv:2606.30049）；监控超分提出以人脸/车牌识别得分替代 PSNR/SSIM（paper:arxiv:2609.39649）；自编码器潜空间余弦相似度被主张替代 MSE/PSNR/SSIM（TID2013 上与 MOS 正相关）（paper:arxiv:2608.24782）。
- **标量盲区实证**：DCT 频谱诊断显示 ~1 bpp 工作点三种 NIC 模型高频重建能量 80–97% 泄漏至目标频带外——PSNR 类标量 RD 指标无法发现此类频谱失真（paper:arxiv:2611.10000）；工业机器视觉联合训练中 PSNR 仅轻微下降但缺陷检测 mAP@50 从 0.461 升至 0.887（paper:arxiv:2611.11831）。
- **生成式路线重返保真轴**：Gen2-VC-DCVC-UF 声称是首个在低码率下 PSNR 与 MS-SSIM 均超越 VTM-23.0 的生成式视频编码器，且匹配 LPIPS 下省码率 86.65%（paper:arxiv:2609.34725）；超低码率图像侧 DiffCR 在 PSNR 口径省 65.1% BD-rate（paper:arxiv:2601.10373）、Gen2-IC 在 <0.05 bpp 区间 PSNR 领先扩散式编解码器（paper:arxiv:2606.21030）。
- 新表征域持续以 PSNR 结算：3DGS 体积视频 SAGA 相对 GIFStream 的 PSNR 口径 BD-rate 降 90.88%（paper:arxiv:2609.33969）；双流高斯泼溅较 V³ 式基线 +7.51–8.35 dB（paper:arxiv:2610.21121）；稀疏视角 4DGS 官方测试集全帧 30.04 dB（paper:arxiv:2610.04606）；事件引导编码 ENVC 相对 DCMVC 以 PSNR-RGB 口径省 39.13% BD-rate（六基准平均）（paper:arxiv:2610.02265）；HR-NVC++ 相对 VTM-13.2（RA）省 13.01% PSNR BD-rate（paper:arxiv:2611.15670）；可逆变换 InnVC 相对 x265 降 21.66% 且单模型覆盖 >20 dB PSNR 范围（paper:arxiv:2606.13957）；屏幕内容 NeR-SC 达 40.32/41.73 dB 并在低码率超越 H.264/H.265（paper:arxiv:2605.27024）。

---

## 当前状态与关注点

**活跃度**：极高。2021 年起每年数十条挂接，覆盖传统编码器、神经编解码（LIC/NVC/INR）、超分与修复、点云、3DGS 体积视频、事件相机、ISP、医学影像、5G 传输（paper:arxiv:2609.25423）等持续扩张的域。统一评测框架（UI-LIC）将 PSNR 与 SSIM/VMAF/LPIPS 并列为核心输出指标（paper:arxiv:2606.23545）。〔档案推断：PSNR 是本知识库中被引用密度最高的度量实体之一，无衰退迹象〕

**开放问题**：
1. **感知–失真鸿沟的持续侵蚀**：锐度（SI-PSNR 修补，paper:arxiv:2608.13989）、语义/诊断可用性（paper:arxiv:2607.26333）、物理可解释性（paper:arxiv:2606.30049）、机器视觉下游效用（paper:arxiv:2611.11831）等场景中 PSNR 与任务目标脱钩；监控域已出现以识别得分全面替代 PSNR/SSIM 的基准（paper:arxiv:2609.39649）。
2. **标量聚合掩盖频谱行为**：80–97% 的频带外能量泄漏不被 PSNR 类指标捕获（paper:arxiv:2611.10000）——频谱级评测是否会成为标配待观察。
3. **BD(PSNR) 的可靠性边界**：标准场景误差 <0.5 pp，但 VMAF/能耗/跨编解码器场景可达 5 pp，且低于子集误差阈值的 BD 值不应下结论（paper:arxiv:2304.12852、paper:arxiv:2401.04039）。
4. **无参考化**：BlindPSNR 与代理参考框架证明 PSNR 可被高精度盲预测（paper:arxiv:2607.27628、paper:arxiv:2607.23321），智能体修复系统已用“预测 PSNR 增益”作接受/停止判据（paper:arxiv:2610.06196）。

**生态位**：
- **保真轴的公共分母**：4K 主观研究确认 PSNR 对神经编解码器仍有效、序列内比较秩相关最高，且传统/神经编解码器间无显著差异（paper:arxiv:2511.00969）——这为跨阵营对比提供了最中立的锚点；但整体 Pearson 相关上 VMAF 更强，两者呈互补分工。
- **变体家族化**：按域分化出 WS-PSNR（360°，paper:arxiv:2402.10257）、点对点 PSNR（paper:arxiv:2308.12535）、仅占用率 PSNR（V-PCC，standard_proposal:jvet:m195-AE0092）、PSNR-HVS（JPEG AI，paper:arxiv:2510.13867）、XPSNR（paper:arxiv:2601.10607）、SI-PSNR（paper:arxiv:2608.13989）；按分量分化出 PSNR-Y/YUV/RGB 口径（paper:arxiv:2408.03265、paper:arxiv:2605.15800、paper:arxiv:2610.02265）。
- **调优权衡轴**：编码器显式提供 tune=PSNR 与 tune VMAF/MS-SSIM 的切换，VMAF 调优以“PSNR 极小损失”为约束表述（repo_release:github:SVT-AV1-v4.2.0）。
- **生成式压缩的回归检验**：生成式路线历史上以牺牲源保真换感知（paper:arxiv:2609.34725 精读），2026 年 Gen2-VC 首次在 PSNR 上超越 VTM-23.0（低码率），标志感知-保真权衡边界被推窄——PSNR 成为检验该进程的标尺。
- 〔档案推断〕生成式视频质量评估（如 WorldJen 的 VLM Likert 体系，paper:arxiv:2605.03475）不依赖参考图像，PSNR 在该新兴场景中暂无直接落点，为其未来适用性留下空白。
