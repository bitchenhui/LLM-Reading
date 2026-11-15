# 标准生态 · 领域综述

> 引擎合成 · 数据截止 2026-11-15 · 基于 1001 条结构化条目 · glm-5.3

# 标准生态（视频编码标准与生态）领域综述

> 数据截止：2026-11-15。本综述基于给定条目（JVET 会议提案、算法描述/草案文本节点、工业动态与论文条目）撰写；条目未覆盖的判断以〔综述推断〕显式标注。

---

## 一、发展历程

以 JVET（ITU-T VCEG + ISO/IEC MPEG 联合组）为主线，2021–2026 年的标准生态可划分为四个阶段，其代际切换遵循“AHG 探索 → EE 探索实验 → CfE → CfP”的程序链条。

### 阶段一：VVC 定稿后的维护与生态奠基（2021-10 ～ 2022）

- **组织形态**：JVET 以常设专题组（AHG1–AHG12）覆盖项目管理、文本编辑、参考软件（VTM）、测试素材、一致性、ECM 软件、HDR/WCG、高位深/高码率/高帧率、SEI、编码优化、神经网络编码（AHG11）、超越 VVC 增强压缩（AHG12）全线工作（standard_proposal:jvet:m188-X0001 ~ m188-X0012）；2022-01 增设胶片颗粒专题组 AHG13（standard_proposal:jvet:m189-Y0013），AHG7 转向低时延与受限复杂度（standard_proposal:jvet:m189-Y0007）。
- **文本节点**：VVC 操作范围扩展草案推进至 Draft 5（standard_proposal:jvet:m188-X2005）、一致性测试 Draft 7（standard_proposal:jvet:m188-X2008）、范围扩展一致性 Draft 2（standard_proposal:jvet:m188-X2026）；VVC v1/v2 一致性测试 BoG 启动（standard_proposal:jvet:m188-X0207）；HEVC 新级别草案 Draft 1→3（standard_proposal:jvet:m188-X1005、m190-Z1005）；AVC/HEVC/视频 CICP 增补色彩类型标识符 Draft 1→4（standard_proposal:jvet:m190-Z1008 ~ m194-AD1008）。跨标准勘误机制每会运行（standard_proposal:jvet:m188-X1004 起系列）。
- **参考软件版本**：VTM 15（standard_proposal:jvet:m188-X2002）→ VTM 17（standard_proposal:jvet:m190-Z2002）→ VTM 18（standard_proposal:jvet:m192-AB2002）；ECM 3（standard_proposal:jvet:m188-X2025）→ ECM 6（standard_proposal:jvet:m191-AA2025）→ ECM 7（standard_proposal:jvet:m192-AB2025）。
- **探索启动**：EE2（超越 VVC 增强压缩）自 2021-10 起每会输出总结（standard_proposal:jvet:m188-X0024、m188-X2024 起系列）；ECM 侧 GDR（standard_proposal:jvet:m189-Y0162、m189-Y0163）、RPR 修复与滤波强化（standard_proposal:jvet:m188-X0121、m190-Z0062、m190-Z0069）密集推进。
- **部署信号**：每会固定发布 HEVC/VVC 部署状态报告（standard_proposal:jvet:m188-X0020、m188-X0021 起系列）；优酷基于 Ali266 的 VVC 流媒体试部署（standard_proposal:jvet:m189-Y0122）、VVenC/VVdeC 持续更新（standard_proposal:jvet:m188-X0044、m189-Y0136）、字节 BVC 异构 CPU+GPU 解码器（standard_proposal:jvet:m189-Y0054）、VVC/HEVC 8K 主观对比（standard_proposal:jvet:m188-X0186）。

### 阶段二：下一代探索机制化与专题扩容（2023）

- **组织扩容**：2023-01 增设 NNVC 软件开发 AHG14（standard_proposal:jvet:m193-AC0014）与面向机器分析（VCM）专题组（standard_proposal:jvet:m193-AC0015）；2023-04 起 AHG7 转为 ECM 工具评估、VCM 落位 AHG8（standard_proposal:jvet:m194-AD0007、m194-AD0008）。
- **ECM 提速与评估体系成型**：ECM 9→11（standard_proposal:jvet:m194-AD2025、m195-AE2025、m196-AF2025）；ECM 主观评估首报（standard_proposal:jvet:m192-AB0270）、ECM/VTM 视觉质量对比（standard_proposal:jvet:m192-AB2029）、分阶段复杂度评估（standard_proposal:jvet:m195-AE0195）、内存消耗系列报告（standard_proposal:jvet:m190-Z0150、m195-AE0180、m196-AF0201）确立“增益+主观+复杂度+内存”四维评估框架。
- **多层 VVC 进入验证测试（VT）**：计划草案（standard_proposal:jvet:m192-AB0123、m192-AB2021）→ 更新 1（standard_proposal:jvet:m195-AE2021）；空间可伸缩性专家观看结果（standard_proposal:jvet:m194-AD0399、m195-AE0288、m196-AF0311）、内容分层报告（standard_proposal:jvet:m196-AF2033）。
- **SEI 与 NN 工具扩张**：Green-MPEG SEI 进 VTM（standard_proposal:jvet:m190-Z0046、m192-AB0072）；SEI 处理顺序消息 Draft 1→6（standard_proposal:jvet:m191-AA2027 ~ m195-AE2027）；NNPF/NNPFC 向 AVC/HEVC 移植（standard_proposal:jvet:m195-AE0101、m196-AF0045）。
- **HEVC 多视点线启动**：苹果提出 HEVC 多视点 Profile（standard_proposal:jvet:m191-AA0239），扩展位深草案 Draft 1→2（standard_proposal:jvet:m191-AA1011、m195-AE296）。
- **外部并行路线**：MPAI-EEV 端到端神经编码标准声称感知指标优于 H.266/VVC（paper:arxiv:2309.07589）；MPEG-5 LCEVC 在 JVET 内对照 HM/VTM 评估并引发多轮交叉验证与异议（standard_proposal:jvet:m196-AF0075、m196-AF0224、m196-AF0228、m196-AF0277、m196-AF0292）。

### 阶段三：应用导向扩张与 CfE 启动（2024 ～ 2025 中）

- **新专题组**：游戏内容压缩 AHG15（standard_proposal:jvet:m197-AG0015）、生成式人脸视频压缩（GFVC）AHG16（standard_proposal:jvet:m197-AG0016）、超越 CTC 测试 AHG17（standard_proposal:jvet:m201-AK0017）、超低时延与丢包韧性 AHG18（standard_proposal:jvet:m202-AL0018）。
- **VVC 版本整合**：第 4 版草案 Draft 8→13（standard_proposal:jvet:m198-AH2005 ~ m203-AM2005）；第 2 版参考软件基线 Draft 1→2（standard_proposal:jvet:m198-AH2009、m200-AJ2009）。
- **ECM 12→20**（standard_proposal:jvet:m197-AG2025 ~ m206-AP2025），配套上下文重训练周期（standard_proposal:jvet:m198-AH0223、m199-AI0281）、工具关断消融（standard_proposal:jvet:m193-AC1711、m193-AC0354）、工具交互分析（standard_proposal:jvet:m202-AL0171）、12 比特内部位深（standard_proposal:jvet:m200-AJ0237、m203-AM0216）。
- **CfE 启动**：2025-03 提出联合 CfE 草案（standard_proposal:jvet:m202-AL0047、m202-AL2026），2025-06 JVET 与 MPEG 联合发布 CfE（standard_proposal:jvet:m203-AM2026）。
- **部署深化**：骁龙 X Elite AI PC 上 4K 120fps VVC 播放（standard_proposal:jvet:m200-AJ0265）、Chromium 播放方案（standard_proposal:jvet:m203-AM0242）、资源受限 4K 超低延迟软件编码演示（standard_proposal:jvet:m203-AM0298）。

### 阶段四：CfE 收束、CfP 发布与组织转段（2025-10 ～ 2026-10）

- **CfE→CfP 闭环**：CfE 修订文本与结果（standard_proposal:jvet:m204-AN2026、m204-AN2029）；多方响应（standard_proposal:jvet:m204-AN0085、m204-AN0198、m204-AN0267）；CfP 草案（standard_proposal:jvet:m205-AO2026、m205-AO0045）→ 最终草案（standard_proposal:jvet:m206-AP2026）→ **2026-07 联合 CfP 正式发布**（standard_proposal:jvet:m207-AQ2021），应征提案描述模板定稿（standard_proposal:jvet:m207-AQ2022、m208-AR2022）。
- **配套基准与口径**：CfE 条件下 ECM/VTM 性能（standard_proposal:jvet:m203-AM0269）、CfE/CfP 用 ECM 基准点（standard_proposal:jvet:m204-AN0272）、CfP VTM 编码规划（standard_proposal:jvet:m206-AP0296）、VTM-24.0 RDO 计数作为 CfP 复杂度报告口径（standard_proposal:jvet:m208-AR0138）、0.2 倍运行时间目标配置（standard_proposal:jvet:m206-AP0237）。
- **组织转段**：ECM 止步于 v20（standard_proposal:jvet:m206-AP2025），其后会议无新版算法描述；2026-10 AHG6 改设为“非参考软件资产”（standard_proposal:jvet:m208-AR0006）——〔综述推断〕ECM 探索线的角色已被 CfP 评估流程取代。硬件实现复杂度专题组于 2026-01 设立（AHG19，standard_proposal:jvet:m205-AO0019）并于 2026-04 起固化为 AHG16（standard_proposal:jvet:m206-AP0016）。
- **多层 VVC 收口**：VT 计划更新至第 8 版（standard_proposal:jvet:m205-AO2021）、主观观看结果与验证测试报告落地（standard_proposal:jvet:m206-AP0268、m206-AP2033）；MV-HEVC 新档位一致性码流交付（standard_proposal:jvet:m207-AQ0186）。
- **许可生态信号**：WIPO 与 Via Licensing Alliance 合作扩展经专利池验证的 SEP 数据（industry_news:viala:wipo-expands-pool-verified-sep-data-with-via-licensing-allia）；Via LA 启动数据中心 DRAM 首个专利池并持续人事布局（industry_news:viala:via-licensing-alliance-formally-launches-first-patent-pool-i、industry_news:viala:via-licensing-alliance-appoints-tony-piotrowski-as-general-c）。

---

## 二、技术主线与代表工作

### 主线 1：VVC 家族的多版本维护与整合
v2（范围扩展/一致性）、第 4 版 Draft 8–13（standard_proposal:jvet:m198-AH2005 ~ m203-AM2005）直至 2025-10 汇入“含扩展与更正的 VVC”新版整合草案 Draft 1（standard_proposal:jvet:m204-AN2001）；一致性规范迭代至 Draft 8（standard_proposal:jvet:m204-AN2008）并启动增补修正草案（standard_proposal:jvet:m202-AL2028）；HM/VTM 通用测试条件（CTC）与软件开发指南形成例行维护（standard_proposal:jvet:m192-AB2010、m201-AK2010、m202-AL2010、m206-AP2010；m193-AC2003、m200-AJ2003）。VVC 结构概念参考指南（standard_proposal:jvet:m204-AN0258）与 MC-IF 技术指南（standard_proposal:jvet:m195-AE0154、m196-AF0175）完善生态知识基线。

### 主线 2：ECM/EE2 超越 VVC 探索
以 ECM 3→20 的版本链为载体，覆盖划分优化与交叉验证（standard_proposal:jvet:m188-X0144、m188-X0196）、模板匹配类帧内工具（standard_proposal:jvet:m191-AA0132、m204-AJ0043、m199-AI0051）、帧间 MTS（standard_proposal:jvet:m190-Z0147）、色度 IBC 回迁（standard_proposal:jvet:m193-AC0080）、GDR（standard_proposal:jvet:m190-Z0118、m190-Z0141）、RPR 编码器控制（standard_proposal:jvet:m196-AF0058、m197-AG0116）、环内滤波（standard_proposal:jvet:m200-AJ0210、m202-AL0225、m203-AM0219）、熵编码上下文与 bin/bit 比率分析（standard_proposal:jvet:m195-AE0147、m203-AM0227、m204-AN0223）。主观验证（standard_proposal:jvet:m198-AH0344、m198-AH2029）与工具消融方法学（standard_proposal:jvet:m193-AC0354）构成证据链。

### 主线 3：神经网络编码三线并进
- **ECM 内嵌 NN 工具**：NN 环路滤波（standard_proposal:jvet:m189-Y0079、m189-Y0098）、NN 帧内预测映射 VVC 模式（standard_proposal:jvet:m192-AB0149、m193-AC0116，三重交叉验证 m193-AC0238、m193-AC0270、m193-AC0298）、CNN 超分+RPR（standard_proposal:jvet:m191-AA0065、m192-AB0077）、统一参考帧合成（standard_proposal:jvet:m199-AI0089、m203-AM0114、m204-AN0084）、轻量多尺度参考帧生成（standard_proposal:jvet:m201-AK0071、m202-AL0104）、NNLF 接口与共享模型评估（standard_proposal:jvet:m201-AK0337、m202-AL0228、m203-AM0176）、张量帧内模式推导进 VTM 与 CfP 响应软件（standard_proposal:jvet:m205-AO0200）。
- **SEI 化 NN 后处理激活存量**：NNPFC 帧率上采样（standard_proposal:jvet:m193-AC0074）、NNPF 扩展 AVC/HEVC（standard_proposal:jvet:m195-AE0101、m196-AF0045）、NNPFC/NNPFA 接口文本（standard_proposal:jvet:m200-AJ0049、m201-AK0053）、VVdeC 实时 NNPF 开源实现（standard_proposal:jvet:m206-AP0130）。
- **端到端学习编解码器入锚**：DCVC-FM / DCVC-RT 作为 EE1 学习型帧内锚点（standard_proposal:jvet:m205-AO0186、m205-AO0191、m206-AP0080，交叉验证 m205-AO0295）。外部 MPAI-EEV 提供非 ITU/ISO 路线对照（paper:arxiv:2309.07589）。

### 主线 4：面向机器与新兴内容
VCM（AHG8）：VVC 工具的机器视觉适用性分析（standard_proposal:jvet:m194-AD0186）、机器消费残差精简（standard_proposal:jvet:m197-AG0217、m198-AH0248）、人机混合消费多层 VVC（standard_proposal:jvet:m197-AG0216、m198-AH0247）；游戏内容（standard_proposal:jvet:m201-AK0081、m201-AK0082）；GFVC（standard_proposal:jvet:m201-AK0068、m202-AL0101）；胶片颗粒（FGC SEI 编辑与网页播放器 standard_proposal:jvet:m198-AH0311、区域特性 SEI 进 VTM TuC standard_proposal:jvet:m203-AM0168）；全息/物波 SEI（standard_proposal:jvet:m195-AE0182、m197-AG0049）；V-PCC 评估指标与承载（standard_proposal:jvet:m193-AC0044、m205-AO0090）。

### 主线 5：HEVC/AVC 存量生态再激活
- HEVC：MV-HEVC 档位（字节跳动+苹果联合提案 standard_proposal:jvet:m197-AG0201，明确空间视频需求）、4:4:4 MV 档位链（standard_proposal:jvet:m199-AI0045、m200-AJ0247、m204-AN0293、m206-AP0242）、子图支持（standard_proposal:jvet:m199-AI0256、m206-AP0263、m207-AQ0188）、分层色度推导（standard_proposal:jvet:m200-AJ0215）、新档位/颜色描述符/SEI 草案序列（standard_proposal:jvet:m195-AE1006 ~ m207-AQ1006）、整合版本草案（standard_proposal:jvet:m204-AN1018 等）、白皮书（standard_proposal:jvet:m199-AI1011、m200-AJ1011）。
- AVC：含扩展与修正的整合草案 Draft 1→6（standard_proposal:jvet:m195-AE1016 ~ m206-AP1016）、附加 SEI 支持 Draft 1→5（standard_proposal:jvet:m201-AK1017 ~ m205-AO1017）、新 SEI 扩展机制（standard_proposal:jvet:m205-AO0212、m205-AO0280）。

### 主线 6：SEI 元数据与治理
绿色元数据、SEI 处理顺序（standard_proposal:jvet:m191-AA2027 系列、HEVC/AVC 移植 m202-AL0210）、SPO/PON 跨规范归属调整（standard_proposal:jvet:m199-AI0146、m204-AN0059）、模态信息 SEI（standard_proposal:jvet:m197-AG0079、m198-AH0049、m201-AK0107）、AI 使用限制（standard_proposal:jvet:m202-AL0062）、数字签名内容（standard_proposal:jvet:m201-AK0194）、目标掩膜/深度/alpha 元数据信令（standard_proposal:jvet:m194-AD0175、m206-AP0229、m206-AP0230）、GSI/显示矩形/打包区域（standard_proposal:jvet:m206-AP0223、m202-AL0138、m202-AL0059）。

### 主线 7：实现部署与许可生态
VVenC/VVdeC（含多层与 NNPF，standard_proposal:jvet:m195-AE0172、m203-AM0239、m206-AP0130）、Ali266（智能手机实时编码与评测 standard_proposal:jvet:m205-AO0221、m206-AP0124）、BVC（直播优化 standard_proposal:jvet:m200-AJ0256）、Ittiam i266 移动部署（standard_proposal:jvet:m206-AP0214）、NHK 广播级多层编码器与浏览器/动态层切换原型（standard_proposal:jvet:m201-AK0274、m207-AQ0190、m207-AQ0191
