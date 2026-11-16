# AVC · 实体档案

> codec:AVC · 数据截止 2026-11-16 · 关联 78 条 · glm-5.3

# AVC（codec:AVC）滚动档案

## 档案概览

| 属性 | 内容 |
|---|---|
| 标识 / 类型 | codec:AVC ／ codec_standard |
| 名称 / 别名 | Advanced Video Coding（H.264、H264、MPEG-4 Part 10） |
| 状态 / 首版 | ratified ／ 2003 |
| 开发方 | org:VCEG、org:MPEG（档案窗口内的维护活动均见于 JVET 会期文档） |
| 谱系关系 | predecessor_of → codec:HEVC |
| 注册表定性 | 部署量最大的标准；视频会议场景（MLVC 对比锚点之一）仍大量使用 |

**档案构成**：挂接条目 78 条 = 55 条 JVET 提案（standard_proposal:jvet:* ，覆盖 m188–m208 约 20 个会期，2021-10 至 2026-10）+ 23 篇 arXiv 论文（paper:arxiv:*，2022-10 至 2026-09）。提案侧无一新编码工具类条目，全部为勘误、SEI/信令扩展与修订草案等维护性质工作；论文侧 AVC 几乎均以基线、锚点或优化宿主身份出现。

## 关键事实与演进

### 2003–2021：基线地位与谱系定位（注册表静态信息）
- 2003 年首版发布；静态关系标注为 HEVC 的前代标准，本身已进入纯维护期。

### 2021-10 – 2022：维护框架成型
- **勘误常态化启动**：自 standard_proposal:jvet:m188-X1004 起，每会期形成一次跨标准（VVC/VSEI/HEVC/AVC/Video CICP）勘误汇总，后续 standard_proposal:jvet:m190-Z1004、m191-AA1004、m192-AB1004 延续，由 Bross、Sullivan、Rosewarne 等主编署名（standard_proposal:jvet:m192-AB1004），构成权威文本修正记录。
- **色彩表示能力扩展**：standard_proposal:jvet:m190-Z1008（草案 1）启动为 AVC/HEVC 增补附加色彩类型标识符，并联动视频 CICP（ISO/IEC 23091-2 码点，见 standard_proposal:jvet:m192-AB1008）；同年 10 月推进至草案 2。
- **等级体系修订输入**：standard_proposal:jvet:m191-AA0222 针对新增等级 6.x 提出运动矢量取值限制的规范化建议，属对既有等级体系的修订方向技术输入。
- 研究侧：复用 H.264 码流运动矢量与残差辅助视频超分对齐，REDS4、CRF=23 条件下计算量节省上限 70%（paper:arxiv:2210.08229）——码流侧信息成为 AVC 生态的二次利用价值点。

### 2023：整合修订启动，研究锚点角色固化
- 色彩标识符推进至第 3 稿（standard_proposal:jvet:m193-AC1008）、第 4 稿（standard_proposal:jvet:m194-AD1008）；此后该独立工作线未再见于档案〔档案推断：已并入整合修订文本〕。
- **7 月，整合修订第 1 稿**：standard_proposal:jvet:m195-AE1016 将 AVC 及其扩展与勘误整合为新版规范草案，标志 AVC 进入新版本文本起草阶段；10 月即出第 2 稿（standard_proposal:jvet:m196-AF1016）。
- **SEI 扩展开闸**：standard_proposal:jvet:m195-AE0101 提出将神经网络后置滤波（NNPF）与相位指示 SEI 扩展至 AVC/HEVC；standard_proposal:jvet:m196-AF0045 进一步讨论 NNPF SEI 在 AVC 码流中的使用方式——神经类 SEI 工具自 VVC/VSEI 生态向既有标准回灌。
- 研究锚点密集出现：分布式深度视频压缩 RD 性能显著优于 H.264（paper:arxiv:2303.11599）；五标准 SR 基准将 H.264 列入编码源（paper:arxiv:2305.04844）；微软 VCD 视频会议数据集在低延迟设置下评测 H.264/H.265/H.266/AV1（paper:arxiv:2309.07376）；MCBE 以 AVC 预测率失真曲线为下界剔除 HEVC/AV1 冗余表示，直播场景累计编码能耗 −56.45%、存储 −94.99%、传输 −77.61%（JND=6 VMAF 点，对比工业基线码率阶梯，paper:arxiv:2310.09570）；无人机 360° 基准纳入 AVC 软硬件编码器（paper:arxiv:2311.00082）。

### 2024：元数据信令扩展与解码端研究
- 1 月 standard_proposal:jvet:m197-AG0079 提出 AVC/HEVC 的 VUI 扩展机制与图像模态信息信令；4 月 standard_proposal:jvet:m198-AH0049 推进模态信息 SEI；4 月整合修订至第 3 稿（standard_proposal:jvet:m198-AH1016）。勘误线持续（standard_proposal:jvet:m199-AI1004、m200-AJ1004）。
- 研究侧：Cool-chic video 将 AVC/HEVC/VVC 定位为"编码端重、解码端轻"范式参照轴（paper:arxiv:2402.03179）；扩散模型极限压缩在低 bpp 区间以 LPIPS/FVD 衡量优于 H.264/H.265（paper:arxiv:2402.08934）；六格式软/硬件解码能效系统评测纳入 AVC（paper:arxiv:2402.09001）；H.264/H.265/VP9 三分辨率各 CRF 档实测 PSNR 20–40 dB，凸包可用对数多项式高精度建模且跨编码器可相互预测（paper:arxiv:2408.09044）；AIM 2024 压缩 VQA 挑战赛 459 条测试视频由覆盖 AVC/HEVC/AV1/VVC 的 14 种编解码器生成（paper:arxiv:2408.11982）。

### 2025：SEI 扩展集中推进年
- AHG9 议题爆发：数字签名内容 SEI（standard_proposal:jvet:m201-AK0194）、AI 使用限制 SEI（standard_proposal:jvet:m202-AL0062）、生成式人脸视频及其增强 SEI（standard_proposal:jvet:m202-AL0148）、SEI 处理顺序 SEI（standard_proposal:jvet:m202-AL0210）、编码器优化跟踪（standard_proposal:jvet:m202-AL0061，LGE）、VSEI 第 4 版 SPO/PON SEI 在 AVC 接口文本中的呈现（standard_proposal:jvet:m204-AN0059）。
- **"AVC 附加 SEI 消息支持"修订线成文**：草案 1（standard_proposal:jvet:m201-AK1017，2025-01）→ 草案 2（standard_proposal:jvet:m202-AL1017）→ 草案 3（standard_proposal:jvet:m203-AM1017）→ 草案 4（standard_proposal:jvet:m204-AN1017）。
- 整合修订线出第 4 稿（standard_proposal:jvet:m204-AN1016）。

### 2026：修订文本成熟与扩展机制工程化
- 1 月：standard_proposal:jvet:m205-AO0212 提出 AVC 新 SEI 消息扩展机制（可扩展性架构级贡献），m205-AO0280 为其编辑研究；整合修订第 5 稿（m205-AO1016）、附加 SEI 草案第 5 稿（m205-AO1017）。
- 4 月：整合修订第 6 稿（standard_proposal:jvet:m206-AP1016）；FGC SEI payloadType 码点讨论（m206-AP0217）、alpha 平面（m206-AP0229）与深度图（m206-AP0230）元数据信令选项。
- 7/10 月：通用 SEI 信令机制跨标准勘误（standard_proposal:jvet:m207-AQ0089）、SeiExtensionEnabledFlag/SeiExtensionBitsPresentFlag 语义一致性探讨（m208-AR0052）、数组与列表初始化条文勘误（m208-AR0184）。
- 研究侧量化（AVC 为锚点/宿主）：
  - H.266 相对 H.264 最高 −71.3% VMAF BD-rate（四数据集×四编码器评测中的最大值，paper:arxiv:2603.26763）；
  - NeuralLVC 在 CIF/720p/1080p 全分辨率无损压缩超越 H.264（Hi444PP 为传统无损锚点，paper:arxiv:2604.03353）；
  - NeR-SC 屏幕内容低码率超越 H.264/H.265，VCD 平均 PSNR 41.73 dB（paper:arxiv:2605.27024）；
  - 离散 VQ 编码 LPIPS 较 H.264 增益 25–52%（128×128、同等或更低码率，paper:arxiv:2607.23366）；
  - **H.264 可微代理自适应量化**：相对固定 QP 的 H.264 基线，语义分割任务 BD-rate −17.12%、MS-SSIM 目标 BD-rate −15.30%（paper:arxiv:2607.10478）——不改码流语法前提下以 AVC 为优化宿主；NRM 集成 RDO 亦在 AVC 上验证（paper:arxiv:2602.15779）；
  - 时域一致性实证将 H.264 列入四编解码器，发现"可预测性异常"（paper:arxiv:2605.18378）；
  - OASIS 指出 H.264/H.265 帧间编码在自动驾驶传感器内链路场景存在高延迟/高复杂度的结构性不匹配（paper:arxiv:2609.15749）。

## 当前状态与关注点

**活跃度**：ratified 23 年后仍处活跃维护，但演进已完全转入维护轨道——档案窗口内（m188–m208）零新编码工具提案，工作收敛于三条线：(1) 每会期跨标准勘误（x1004 系列及 AHG 专项，主编署名具权威性）；(2) "AVC 含扩展与修正"整合修订，已迭代至第 6 稿（standard_proposal:jvet:m206-AP1016）；(3) "附加 SEI 消息支持"修订，已至第 5 稿（standard_proposal:jvet:m205-AO1017）并配套 SEI 扩展机制提案（m205-AO0212/0280）。

**开放问题**：
- 两条修订草案线截至窗口末（2026-10）仍处草案迭代，最终版发布时点未见于档案；
- 色彩类型标识符工作 4 稿后（2023-04）无单独后续记录〔档案推断：并入整合修订文本〕；
- 等级 6.x 运动矢量限制仅一次提案输入（standard_proposal:jvet:m191-AA0222），采纳状态未知；
- 多项 SEI 议题（alpha/深度元数据、模态信息、数字签名、AI 使用限制、生成式人脸标注）尚处 AHG9 进展报告阶段，未进入标准文本修订。

**生态位**：
- **部署面**：注册表定性"部署量最大"；视频会议场景仍大量使用并为 MLVC 对比锚点之一，VCD 低延迟评测实证该地位（paper:arxiv:2309.07376）；
- **研究角色双面性**：一方面作为"被超越的下界锚点"——压缩效率被 H.266 拉开最高 −71.3% VMAF BD-rate（paper:arxiv:2603.26763），并在感知、无损、屏幕内容等维度被神经方案超越（paper:arxiv:2402.08934、2604.03353、2605.27024）；另一方面其稳定语法与码流结构被持续复用为超分对齐信息源（paper:arxiv:2210.08229）、率控优化宿主（paper:arxiv:2607.10478、2602.15779）与流媒体能耗基准曲线（paper:arxiv:2310.09570）；
- **演进策略**：能力更新集中于 SEI 元数据层（NNPF、色彩标识符、内容签名、AI 使用治理、生成式内容标注），反映标准组织让最大存量部署标准承载 AI/生成式时代元数据需求的路线（standard_proposal:jvet:m202-AL0062、m202-AL0148 等）；
- **边界场景**：帧间编码范式在高实时、低功耗前端（车载传感器内压缩）被指出结构性不匹配（paper:arxiv:2609.15749），提示 AVC 强项仍在传统传输/存储链路而非新兴边缘感知管线。
