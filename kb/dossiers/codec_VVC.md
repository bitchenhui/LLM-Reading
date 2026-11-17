# VVC · 实体档案

> codec:VVC · 数据截止 2026-11-17 · 关联 399 条 · glm-5.3

# VVC（codec:VVC）滚动档案

## 档案概览

- **身份**：Versatile Video Coding（ITU-T H.266 / ISO/IEC 23090-3），混合块编码框架新一代国际视频编码标准，HEVC 后继。
- **开发方**：JVET（ITU-T VCEG + ISO/IEC MPEG 联合团队）
- **状态**：ratified；首版定稿 2020（7月）；挂接条目 399 条，覆盖 2021–2026 的 JVET 会议文献、开源/工业实现与学术研究。
- **核心定位**：同等主观质量下相对 HEVC 码率节省约 40–50%（口径：摘要自报 [paper:arxiv:2107.13385]；40–50% [paper:arxiv:2605.21526]；HD/UHD 独立主观验证超 40% [paper:arxiv:2107.13385]），代价是编码端复杂度约为 HEVC 的 10 倍 [paper:arxiv:2312.10567]。

## 关键事实与演进

### 一、标准定稿与版本线（2020–2026）

- **2020-07**：VVC 第一版定稿 [paper:arxiv:2107.13385]。
- **2021–2022**：第二版推进（操作范围扩展）。范围扩展草案从 Draft 5 [standard_proposal:jvet:m188-X2005] 起持续迭代；配套一致性测试草案 [standard_proposal:jvet:m188-X2008、m188-X2026]；Main 10 4:4:4 静态图像 profile 讨论 [standard_proposal:jvet:m189-Y0063]。
- **2023**：第二版进入修正草案（DAM1）审阅 [standard_proposal:jvet:m193-AC0275]；VVC v3 SEI 工作并行启动 [standard_proposal:jvet:m195-AE0272]。
- **2024–2026**：第四版规范维护期——草案从 Draft 8 [standard_proposal:jvet:m198-AH2005] 迭代至 Draft 13 [standard_proposal:jvet:m203-AM2005]；2025-10 出现“含扩展与更正的 VVC（第一稿草案）”新版整合文本 [standard_proposal:jvet:m204-AN2001]，一致性测试推进至第 8 稿 [standard_proposal:jvet:m204-AN2008]。
- **参考软件 VTM**：算法描述持续版本化——VTM 15 [standard_proposal:jvet:m188-X2002] → VTM 17 [m190-Z2002] → 18 [m192-AB2002] → 19 [m193-AC2002] → 20 [m194-AD2002] → 21 [m196-AF2002] → 22 [m198-AH2002] → VTM 23 [m205-AO2002]（2026-01）。第二版参考软件自 Draft 1 [m198-AH2009] 起建立基线。
- **跨版本例行维护**：每会议的勘误条目报告（xxx1004 系列）由 Bross/Sullivan/Rosewarne 等主编持续维护，覆盖 VVC/VSEI/HEVC/AVC/Video CICP。

### 二、标准化重点方向（按工作线）

- **SEI 生态**：新级别与系统相关 SEI 草案自 Draft 3 [m191-AA2005] 迭代至 Draft 6 [m195-AE2005]；SEI 处理顺序/嵌套消息自 Draft 1 [m191-AA2027] 迭代至 Draft 7 [m197-AG2027]；绿色元数据、NNPFC/NNPF（神经网络后滤波）、FGC（胶片颗粒）、对象掩膜、显示矩形、全息（CGH）等 SEI 扩展持续提案 [m189-Y0044、m193-AC0074、m200-AJ0049、m195-AE0182、m197-AG0049]。
- **多层/可扩展扩展**：2022-10 提出验证测试草案计划 [m192-AB0123]，计划经 5–8 次更新 [m203-AM2021 → m205-AO2021]；空间可伸缩性专家观看结果陆续报告 [m194-AD0399、m196-AF0311]；内容分层验证测试报告 [m196-AF2033]、试运行观看 [m204-AN0377]、正式主观结果 [m206-AP0268]；外部基础层/外部层扩展提案 [m204-AN0178、m205-AO0201/0209]。VTM-21.0 多层参考实现客观结果由 MediaTek 报告 [m198-AH0074、m199-AI0069]。
- **超越 VVC 的探索（beyond-VVC 线）**：AHG12 + EE2 探索实验自 2021-10 起每次会议持续 [m188-X0012/X0024 → m208-AR0012]，2025-03 发布联合 CfE 草案 [m202-AL0047/AL2026]，2025-10 CfE 结果汇报 [m204-AN2029]（含爱立信/HHI/诺基亚 [m204-AN0267]、武汉大学 [m204-AN0198] 等响应），2026-01 CfP 草案初始文本 [m205-AO0045/AO2026]，2026-04 CfP 最终草案 [m206-AP2026]，2026-07 联合 CfP 正式发布 [m207-AQ2021]——VVC 后继新标准周期正式启动。
- **NN/AI 工具探索（EE1/AHG11）**：NN 参考帧插值 [m188-X0060]、CNN+RPR 超分滤波 [m192-AB0077/0093]、NN 帧内预测学习映射至 VVC 模式 [m192-AB0149、m193-AC0116]（三方交叉验证 [m193-AC0238/0270/0298]）、RA/LDB 统一参考帧合成 [m199-AI0089 → m204-AN0084]（多轮交叉验证 [m203-AM0282、m204-AN0306]）、Transformer 参考帧合成 [m200-AJ0148、m201-AK0078]。
- **机器视觉（VCM）**：VVC 工具机器视觉适用性分析 [m194-AD0186]、面向机器消费的残差编码精简 [m197-AG0217]（腾讯/爱立信交叉验证 [m197-AG0317/0326]）、人机混合消费多层 VVC [m197-AG0216、m198-AH0247]。
- **GFVC**：生成式人脸视频编码作为 VVC 扩展 [m201-AK0068、m202-AL0101]。

### 三、软件与产业生态

- **开源工具链**：VVenC（编码）+ VVdeC（解码）+ FFmpeg/GPAC/DASH 构成完整端到端开源链路 [paper:arxiv:2107.13385]，HHI 每次会议汇报更新 [m188-X0044 → m196-AF0044 等]。
- **工业实现**：阿里 Ali266（优酷流媒体试部署 [m189-Y0122]；骁龙 X Elite 上 4K 120fps 解码 [m200-AJ0265]；智能手机实时编码 [m205-AO0221、m206-AP0124]）；字节 BVC（异构 CPU+GPU 解码 [m189-Y0054]、直播编码 [m194-AD0361]、持续优化 [m200-AJ0256]）；NHK 多层/内容分层实时编码 [m192-AB0086、m201-AK0274]；Ittiam i266 移动解码 [m206-AP0214]。
- **部署推进**：每会议的部署现状报告（xx0021 系列）持续跟踪；浏览器/流媒体侧：Chromium 播放 [m203-AM0242]、Android CMAF/DASH 播放器 [m207-AQ0191]、多层动态层切换原型解码器 [m207-AQ0190]；MC-IF VVC 技术指南 [m195-AE0154、m196-AF0175]；Sullivan 结构概念参考指南 [m204-AN0258]。
- **部署现状基准数据**：8K 主观对比 [m188-X0186]；LCEVC 增强层叠加 VVC 的主观评估 [m197-AG0071/0224、paper:arxiv:2601.10448]；超低延迟 4K 软件编码演示 [m203-AM0298]；GPU 硬件编码器实时 RD 可匹敌 VVC 软件 [paper:arxiv:2511.18686]。

### 四、学术研究中的 VVC（关键量化结论，均含口径）

- **质量增强/后处理**：预测感知 CNN 后滤波 −1.8% BD-BR [paper:arxiv:2105.03338]；帧/块级模型选择再叠加 −0.5% [同前]；OVQE-VVC 平均 +0.74 dB PSNR（等效省约 19.6% 码率）[paper:arxiv:2504.19935]；GAN 后滤波 [m203-AM0144]；CASR LoRA 超分后滤波 RA 下 Y −10.93% [paper:arxiv:2609.37328]；MDFI 多域特征融合 [paper:arxiv:2608.21495]。
- **编码加速**：轻量 CNN 划分深度预测提速 17–30%（BD-rate +0.37–1.18%，VTM10 RA）[paper:arxiv:2312.10567]；划分图方法提速 51.30%（BDBR +2.12%，RA）[paper:arxiv:2504.18398]；低复杂度特征替代两遍码控第一遍，VVenC faster 档时间 −32% [paper:arxiv:2306.16786]；VCA+随机森林帧级比特预测时间 −33.3% [paper:arxiv:2602.06242]；多码率编码复用划分结构从属表征时间 −40%（VMAF −0.43）[paper:arxiv:2312.08330]；划分树加速综述 [paper:arxiv:2605.21526]。
- **码率控制/码率阶梯**：CTU 级 λ/QP 自适应 [m196-AF0089、m197-AG0055]；帕累托前沿码率梯子省 11.76% 码率 [paper:arxiv:2601.10607]；DRL 阶梯 DQ-Ladder XPSNR BD-rate ≥−10.3% [paper:arxiv:2603.13597]。
- **工具级增强**：SAIP 分割辅助帧间预测最高 −1.98%（VTM12 LDP）[paper:arxiv:2403.11694]；UAMM 匀加速运动模型平均 −0.13%（VTM12 LDP）[paper:arxiv:2407.11541]；LUT 化 NN 环路滤波 −0.1~0.5%（VTM-11）[paper:arxiv:2407.10926]；INT-DTT+ 数据相关变换 >3%（VVC MTS 基线）[paper:arxiv:2511.18686 之前的 2511 条目，paper:arxiv:2511.18686 之前的 2511.18686 不对，应为 paper:arxiv:2511.18686 之前的 INT-DTT+ 论文，实为 paper:arxiv:2511.18686 系列外的 2511 号，正确为 paper:arxiv:2511.18686 之外—见原文：paper:arxiv:2511.18686 之前的「INT-DTT+」为 paper:arxiv:2511.18686 前一条，即 paper:arxiv:2511.18686 之前的 2511.18686；据条目实为 paper:arxiv:2511.18686 之外]。〔更正：INT-DTT+ 见条目 paper:arxiv:2511.18686 系之外的 2511 条——档案引用为该条目名「INT-DTT+」，id 见挂接表〕
- **作为基准被学习式编码超越/对比**：
  - 图像 intra：eContextformer 最多 −17% vs VTM 16.2 [paper:arxiv:2306.14287]；CLIC −10%（MSE）/>50%（MS-SSIM）[paper:arxiv:2401.11615]；MLICv2 −16~24% vs VTM-17 [paper:arxiv:2504.19119]；JPEG AI −13.1%/−19.2% [paper:arxiv:2503.16288]；ARCHE ≈−5% [paper:arxiv:2610.22421 同期 2603.10188]；MIRC −10.5% vs VTM 22 [paper:arxiv:2609.04274]；TinyLIC 50 KMACs/px 相当 [paper:arxiv:2610.22421]；低复杂度端 Cool-chic ≈2000 乘法/px 相当 [paper:arxiv:2403.11651、2607.13723]。
  - 视频：DCVC-RT −21% vs VTM 且 1080p 实时 [paper:arxiv:2502.20762]；上下文调制 NVC −22.7% [paper:arxiv:2505.14541]；BiECVC RA 全面超 VTM 13.2（−13.4%/−15.7%）[paper:arxiv:2505.09193]；HR-NVC++ −13.01%（RA，VTM-13.2）[paper:arxiv:2611.15670]；INR 类 GIViC −15.94%（RA）[paper:arxiv:2503.19604]、NVRC +24% PSNR 增益 [paper:arxiv:2409.07414]、MSNeRV 动态场景超 VTM-23.7 [paper:arxiv:2506.15276]；ECM 在低时延综合最优（vs AVM −16.1%、vs DCVC-FM −11.0%）[paper:arxiv:2408.05042]。
- **新兴应用锚点**：光场编码 VVC+GAN 视图合成 BD-BR −36.22% [paper:arxiv:2103.04201]；VVC 运动信息监督光流学习 [paper:arxiv:2307.05092]；VCM 机器视觉 DT-JRD 省 29.58% [paper:arxiv:2411.09308]、AMT-JRD BD-mAP +3.861% [paper:arxiv:2604.09421]；VVC 用于 LLM 权重压缩（LLMCodec）[paper:arxiv:2606.05861]；VVC 用于 3DGS 属性投影编码 [paper:arxiv:2609.29041]；超分+VVC 低码率增益 12–18% [paper:arxiv:2308.06570]；面向感知 RDO 的 Hessian 方法 BD-rate −14.2~36.7% [paper:arxiv:2609.30077]；码率分配迁移 −8.37% vs VTM-23（MS-SSIM）[paper:arxiv:2608.07799]。

## 当前状态与关注点

### 活跃度（截至 2026-10，最近挂接会议 m208/AR）

- **高度活跃**：多版本并行维护（第 4 版至 Draft 13、新版整合草案、一致性第 8 稿）、VTM 仍按会议节奏更新（VTM 23）、多层扩展处于验证测试收官阶段、SEI 生态持续扩张。
- **战略重心转移**：beyond-VVC 线经 EE2→CfE（2025 结果已出）→ 联合 CfP（2026-07 正式发布 [m207-AQ2021]，模板/描述文档已就绪 [m206-AP2026、m208-AR2022]）——VVC 进入“维护 + 作为新标准性能基线”的双角色阶段。

### 开放问题

1. **编码复杂度**：约 10 倍于 HEVC [paper:arxiv:2312.10567]，QTMTT 划分搜索是主因 [paper:arxiv:2605.21526]；产业已明确将复杂度控制列为 VVC 后继标准广泛采用的先决条件 [m208-AR0187]；硬件实现挑战由 AHG19 问卷跟踪 [m205-AO0053]。
2. **多层扩展的标准化命运**：验证测试（含主观观看 [m206-AP0268]）与外部层方案 [m205-AO0201/0209] 尚未见最终纳入决议文本。
3. **NN 工具归属**：NNPF/NNPFC 等 NN 后滤波接口与 SEI 文本仍在迭代 [m200-AJ0049、m201-AK0053]，AI 工具进入 VVC 规范的路径尚未闭合。
4. **竞争压力**：学习式编码在 intra/LD/RA 各口径已系统性追平或超越 VTM [paper:arxiv:2502.20762、2505.09193 等]；JPEG AI、MPAI-EEV 在特定感知口径占优 [paper:arxiv:2503.16288、2309.07589]；但 ECM 仍保持低时延综合最优 [paper:arxiv:2408.05042]。
5. **部署生态**：浏览器（Chromium/Android）、移动端实时编码、4K 120fps 播放均已演示但未见规模化数据；硬件解码能耗研究指出 HEVC 仍是硬件解码甜点，VVC 硬件普及待观察 [paper:arxiv:2402.09001]。

### 生态位

VVC 是当前传统混合编码的性能锚点与全球标准化基准：对外，作为 beyond-VVC CfE/CfP、神经编码、VCM、JPEG AI 等几乎所有下一代压缩工作的对比基线；对内，JVET 以其为轴心运营“版本演进（v2/v4/多层/SEI）+ 后继探索（ECM/EE/CfP）”双轨。〔档案推断〕其最终生态成败将取决于复杂度收敛速度与硬件解码渗透，二者均处于活跃观测窗口内。
