# HEVC · 实体档案

> codec:HEVC · 数据截止 2026-11-16 · 关联 194 条 · glm-5.3

## 档案概览

| 字段 | 内容 |
|---|---|
| 标识 | codec:HEVC｜High Efficiency Video Coding（别名 H.265 / H265） |
| 状态 | ratified，first_release: 2013 |
| 开发方 | org:JCT-VC |
| 谱系 | successor_of→codec:AVC；predecess_of→codec:VVC（注册表拼写照录） |
| 生态注记 | 学习式编码器现阶段最常用的「可部署 baseline」参照系 |

档案 194 条挂接（2017–2026），三条主线交织：① 开源编码器 Kvazaar 版本线（编码器侧工具演进）；② JVET 标准维护与扩展（部署报告、勘误、档次/级别/SEI/多视点扩展、第 3 版整合文本）；③ 学术文献中作为基准锚点的高频引用——涵盖学习式压缩、能耗评测、质量指标与数据集构建。

## 关键事实与演进

**2013–2020｜定稿与编码器侧演进**
- 2013 年标准定稿（注册表）。开源实现 Kvazaar 逐步成熟：v1.2.0（2017-11）全预设提速 1.19–1.28×，快速预设 BD-Bitrate 最多 -14.8%，新增加密与 360° 自适应 QP [repo_release:github:kvazaar-v1.2.0]；v1.3.0（2019-07）0-uf 档 BD-Bitrate 总平均 -22.7%（vs v1.2），但 8-vs 档速度降至 0.35×，体现压缩-速度权衡 [repo_release:github:kvazaar-v1.3.0]；v2.0.0（2020-04）引入 OBA 码控与 VAQ，BD-Bitrate -15.4%～-31.1%（hevc-D@2-vf 达 -37.4%），新增 16 帧层级 GOP [repo_release:github:kvazaar-v2.0.0]。
- 2020-07 后继标准 VVC 定稿，相同主观质量下较 HEVC 码率降低约 50% [paper:arxiv:2107.13385]——HEVC 自此转入「成熟维护 + 被比较」阶段。

**2021｜部署报告机制启动，学习式方法首次大规模对标**
- JVET-X0020（2021-10）Sullivan 提交首份部署状态报告，此后形成跨 2021-10 至 2026-04 的例会序列（Y0020→…→AP0020）；勘误序列（x1004 系）同步每会维护。
- 级别扩展起草启动（X1005 draft 1）[standard_proposal:jvet:m188-X1005]；X0186 完成 8K 分辨率 VVC/HEVC 主观质量评估。
- 学术侧：NTIRE 2021 质量增强挑战赛（482 队注册）以 HEVC 固定 QP 视频为对象 [paper:arxiv:2104.10781]；SRVC 同等 PSNR 下 bpp 仅为 H.265 slow 模式 16% [paper:arxiv:2104.02322]；M-SRGAN 集成 HM 16.20，VMAF 口径 BD 码率节省 35.6%（JVET CTC UHD/RA）[paper:arxiv:2106.08147]。

**2022｜级别/色彩扩展与多视点启动**
- 新级别草案迭代至 draft 3（Z1005）；附加色彩类型标识符启动（Z1008 draft 1，后续 AB/AC/AD1008 迭代至第四稿）。
- 苹果提出 HEVC 多视点 Profile [standard_proposal:jvet:m191-AA0239] 及扩展位深多视图档次 draft 1 [standard_proposal:jvet:m191-AA1011]——MV-HEVC 档位线由此发端。
- 腾讯 Z0109 在 HEVC/VVC/AV1 内容上评估客观质量指标，HEVC 成为跨标准质量度量的标定内容之一。
- NTIRE 2022 发布 LDV 2.0（335 段），赛道仍锚定 HEVC 压缩视频增强与超分 [paper:arxiv:2204.09314]。

**2023｜档次/SEI 现代化 + 神经增强与实时宣称**
- 新简档/颜色描述符/SEI 消息草案启动（AE1006 draft 1，后续 AF1006→AM1006 迭代）；AE0101 提出将神经网络后置滤波与相位指示 SEI 扩展至 AVC/HEVC——神经增强进入标准化路径；AC0204 规范 HM 参考软件开发指南。
- 字节跳动提交 MV-HEVC profile 提案 [standard_proposal:jvet:m196-AF0063]，2024-01 与苹果联合提案 [standard_proposal:jvet:m197-AG0201]。子图支持首次提出（AI0256）。
- 学习式编解码器对标白热化：MobileNVC 实现移动端 1080p 实时解码、较此前端侧最多省 48% BD-rate [paper:arxiv:2310.01258]；跨平台 NVC 较 H.265 最多省 24.2% 码率 [paper:arxiv:2309.11276]；光场压缩较 HEVC 帧内平均 -62.57% BD-rate [paper:arxiv:2305.00489]；小波 MCTF 较 HEVC 最高省 21% [paper:arxiv:2305.16211]；过拟合图像编码以 2300 次乘法/像素超越 HEVC [paper:arxiv:2307.12706]。
- 能耗格局实证确立：硬件解码中 HEVC 为能耗甜点（vs VP9 能耗 +6.06%，AV1 则 +117.50%），软件解码甜点为 AV1 [paper:arxiv:2402.09001]；无人机 360° 基准中 HEVC 硬件实现取得效率-复杂度最佳折中 [paper:arxiv:2311.00082]。

**2024｜第 3 版整合与空间视频驱动的多视点**
- AH1006「含扩展与修正的 HEVC（第 3 版草案）」启动版本整合；AI1011/AJ1011 白皮书由核心编辑团队再版。
- 苹果 4:4:4 MV-HEVC 档位提案（AI0045、AJ0247），AJ0214 汇总 RExt 多视档位与 4:4:4 支持现状。
- 对标维度继续拓宽：Promptus 较 H.265 节省 >4× 带宽（同等感知质量）[paper:arxiv:2405.20032]；扩散模型极限压缩在 0.02 bpp 区间以 LPIPS/FVD 优于 H.264/H.265 [paper:arxiv:2402.08934]；ODVista 数据集以 HEVC 压缩伪影为核心构造（200 条全景、4 码率档）[paper:arxiv:2403.00604]；Cool-chic 微型解码器以约 300 次乘法/像素仍优于 HEVC [paper:arxiv:2403.11651]；HM-18.0 被用作 JPEG AI 伪影判定的传统编码锚点 [paper:arxiv:2411.06810]。

**2025｜AI 治理类 SEI 密集出现**
- SEI 扩展呈治理化转向：AI 使用限制 SEI（AL0062）、生成式人脸视频 SEI（AL0148）、数字签名内容 SEI（AK0194）、编码器优化信息 SEI（AL0057/AL0061）、SEI 处理顺序（AL0210）、全向视口（AN0071）、3DRD/MAI 深度信息（AN0072）等并进。
- 「含扩展与修正的 HEVC」新文本线启动（AL1018 d1→AM1018 d2→AN1018 d3）；附加档次/SEI 线推进至 d4（AM1006）。
- Kvazaar v2.3.2（2025-09）修复 10-bit 与 SMP/AMP 代价计算，veryslow 预设 BD-BR(PSNR) 较 v2.3.1 降 2.7%（速度 0.77×）[repo_release:github:kvazaar-v2.3.2]。
- AM0298 演示资源受限下 VVC/HEVC 软件 4K 超低延迟实时编码；HyGT 作为 HEVC 扩展取得平均 6% 码率节省、内存较 KLT 少 6.8× [paper:arxiv:2505.21728]；位置相关预测组合在 AI 配置较 HEVC 省 2.0% [paper:arxiv:2505.23672]。

**2026｜一致性验证收尾与档位新草案**
- MV-HEVC 扩展进入符合性阶段：AQ0186 提交多视图单色 10/12-bit 与 4:4:4 10/12-bit 档位一致性比特流，AP0243/AP0244 配套 HM 修复与测试码流；AQ0187 提议在 dev-multiview444 分支整合 SHVC 支持。
- 附加档位新一轮草案（AP1006 d1→AQ1006 d2）；子图支持持续（AP0263/AQ0188，对标 VVC 子图能力）；AO0201 提出外部 HEVC 基本层 + VVC 增强层的双层可分级架构。
- 学术侧标志性结果：码率分配迁移使 HEVC 系编码器 MS-SSIM 口径较 JM-19.0 省 20.20%、较 HM-16.20 省 8.25% [paper:arxiv:2608.07799]；Blackwell GPU 上 8K 10-bit 4:2:2 HEVC 四路分帧编码达 122 fps（SFE 率失真代价 ≤5% BD-Rate）[paper:arxiv:2606.29179]；ReLViC 在严重丢包下优于 RS-FEC 保护的 H.265 [paper:arxiv:2608.30202]；NeuralLVC 无损压缩超越 H.265 RExt 无损模式（CIF/720p/1080p 全分辨率）[paper:arxiv:2604.03353]。

## 当前状态与关注点

**活跃度**：标准本体早已 ratified，但维护面高度活跃——部署报告（2021-10 起跨 18+ 次会议）、跨标准勘误（VVC/VSEI/AVC/CICP 联合条目）形成稳定例会节奏；同时并行至少四条实质性扩展文本线（附加档次/SEI、含扩展与修正新版、MV-HEVC 一致性、子图支持），2026 年仍处于草案迭代与一致性验证阶段。

**生态位**（三重角色）：
1. **硬件护城河**：硬件解码能耗甜点 [paper:arxiv:2402.09001]、360° 场景效率-复杂度最佳折中 [paper:arxiv:2311.00082]、现代 GPU/SoC 硬件编码器实时 RD 可匹敌软件编码器 [paper:arxiv:2511.18686]——与 VVC 约 40–50% BD-rate 增益 [paper:arxiv:2605.21526] 但约 10× 编码复杂度 [paper:arxiv:2312.10567] 的代际格局共同解释了 HEVC 的长尾部署。
2. **评测基座**：学习式编码的通用参照锚（注册表 notes）；HM-18.0 充当神经压缩伪影判定基准 [paper:arxiv:2411.06810]；NTIRE/LDV、ODVista、VCD、AIM 2024（14 种编解码器含 HEVC 系）等数据集以其伪影谱系为构造基础。
3. **系统层承载**：V-PCC 复用 HEVC 压缩点云投影 [paper:arxiv:2207.12554]，高保真 V-PCC 推动商用 GPU 8K 4:2:2 HEVC 实时编码能力验证 [paper:arxiv:2606.29179]。

**开放问题与关注点**：
- **MV-HEVC 4:4:4/单色高档位**：苹果空间视频场景直接驱动 [standard_proposal:jvet:m197-AG0201]，2026 已到一致性比特流阶段，接近定稿——档案内最接近收口的扩展线。
- **AI 时代 SEI 治理**：AI 使用限制、生成式人脸视频、数字签名等能否从 AHG9 进展报告落地为规模化互操作点，决定 HEVC 在 AIGC 内容管线中的元数据地位。
- **学习式方法的侵蚀面**：无损 [paper:arxiv:2604.03353]、极低码率感知（<0.05 bpp）[paper:arxiv:2604.08329]、屏幕内容 [paper:arxiv:2605.27024]、4K LPIPS [paper:arxiv:2609.14129] 等细分维度被逐一宣称超越；但过拟合路线仅以 300–2300 次乘法/像素逼近 HEVC [paper:arxiv:2307.12706][paper:arxiv:2403.11651][paper:arxiv:2501.16976]，解码复杂度竞赛仍在 HEVC 划定的量级下限附近——HEVC 的 baseline 地位短期内未被实质动摇。
- **架构演进方向**〔档案推断〕：双层「HEVC 基本层 + VVC 增强层」可分级提案 [standard_proposal:jvet:m205-AO0201] 与子图支持共同暗示，HEVC 的长期角色更可能是兼容承载层与 VVC 并存，而非被线性替换；此判断需以后续会议采纳结果核实。
