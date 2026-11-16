# MPEG · 实体档案

> org:MPEG · 数据截止 2026-11-16 · 关联 25 条 · glm-5.3

# org:MPEG 滚动档案

## 档案概览

| 项 | 内容 |
|---|---|
| 实体 | ISO/IEC JTC 1/SC 29 Moving Picture Experts Group（别名 ISO/IEC MPEG），kind: standards_body |
| 档案窗口 | 2021-06 至 2026-10，挂接条目 25 条（学术论文 23、标准化提案 2，后者均为 JVET 跨组织提案） |
| 资料刻画的技术域 | 点云压缩（G-PCC/TMC13、V-PCC/TMC2、GeS-TM、V3C）、视频编码（VVC/VTM/ECM、Green-MPEG、多层编码）、面向机器的编码（VCM/FCM）、沉浸式视频（MIV/TMIV）、动态网格（V-DMC/V-Mesh）、高斯泼溅（GS 编码，启动期）、流媒体传输（MPEG-DASH） |
| 生态关系 | 与 JVET 协同（Green-MPEG SEI 在 VTM 落地）；与 JPEG Pleno（点云）、AOM（AV1/AVM、网格编码）、AVS PCC 构成竞争/对标关系 |

档案构成说明：本档案对 MPEG 的刻画几乎全部来自以其标准、参考软件、CTC 与数据集为评测对象的外部研究文献，仅 2 条为 JVET 侧过程性提案，无 MPEG 会议文档一手条目——标准内部进程的时间刻画依赖文献时间戳与版本号侧写。〔档案推断〕

## 关键事实与演进

### 奠基期事实（2017–2021，由后续文献回溯）

- MPEG 自 **2017 年启动 3D 点云压缩标准化**，形成投影式 V-PCC（TMC2，3D 点投影 2D 补丁复用 HEVC/VVC）与几何式 G-PCC（TMC13，八叉树/trisoup + RAHT/predlift 属性变换）两线 [paper:arxiv:2503.17467 摘录] [paper:arxiv:2207.12554 摘录]；统一体积帧框架 **V3C = ISO/IEC 23090-5:2021**，当前含 V-PCC 与 MIV 两标准 [paper:arxiv:2504.05888 摘录]。
- G-PCC 属性压缩的增量式工具改进起点：帧内预测原仅基于距离相似性，引入法向量夹角优化预测子选择后，LiDAR 无损属性编码平均增益 **2.1%**（相对 G-PCC 锚点）[paper:arxiv:2106.12236]。

### 2022：学习式方法挤压锚点 + Green-MPEG 软件化 + JPEG Pleno 竞争显性化

- 学习式八叉树熵模型 OctAttention 较此前 SOTA 取 **10%–35% BD-Rate 增益**（基准含 SemanticKITTI、MPEG 8i、MVUB），较体素基线省 **95%** 编码时间 [paper:arxiv:2202.06028]。
- 动态点云几何帧间深度方案相对锚点差距拉大：vs G-PCCv20 Octree **>88%**、vs Trisoup **>56%**、vs V-PCC intra **>62%** BD-Rate 降低（动态点云几何有损口径）[paper:arxiv:2207.12554]。
- **JPEG Pleno 点云 CfP 竞争**：IT/IST/IPLeiria 学习式几何编解码器在 CfP 测试集上优于 G-PCC、与 V-PCC Intra 相当或更优；几何+颜色联合编解码因质量饱和效应未达几何编解码器水平（该效应遗留为开放问题）[paper:arxiv:2208.02716]。
- **Green-MPEG 能效元数据信令进入 VTM**：SEI 消息的 VTM 软件实现先后两次提案落地（2022-04 [standard_proposal:jvet:m190-Z0046]、2022-10 编码器侧实现 [standard_proposal:jvet:m192-AB0072]），属跨组织过程性贡献而非编码工具。
- VCM 时间线（文献回溯）：MPEG **2019 年发起 VCM**；Track 2（图像/视频压缩）CfP 于 2022-04、Track 1（特征压缩）CfP 于 2023-04 发布 [paper:arxiv:2306.16670 摘录]。

### 2023–2024：机器编码、INR 冲击 MIV、跨标准主观对比、低时延基准

- VCM 特征压缩：端到端多尺度模型较先前特征压缩方法 **≥52% BD-rate 降低**（目标检测任务），编码时间较 VVC 基方案减少 **×5–×27**；先前 VVC 基方案相对 MPEG-VCM 特征锚点最高 96% BD-rate 降低 [paper:arxiv:2306.16670]。
- MPEG-DASH 作为网络研究载体：DRL+INT 遥测的动态 AQM 在 P4 测试环境 MPEG-DASH 场景中卡顿最多降 **90×**、高分辨率播放质量最高升 **42×**（对比固定阈值 AQM 基线）[paper:arxiv:2310.18159]。
- MIV 受 INR 冲击：首个沉浸式 INR 编码器 MV-HiNeRV 在 MPEG MIV CTC 下相对 TMIV（内置 VVenC）最高节省 **72.33%** 码率（论文自报）[paper:arxiv:2402.01596]。
- **首个 MPEG PCC vs JPEG Pleno PCC 主观对比**：两标准各 3 种码率分配策略 × 4 个目标码率，2 种主观评估协议 [paper:arxiv:2402.04760]。
- 低时延配置跨阵营基准：JVET ECM 在 VTM/ECM/libaom/AVM/DCVC-DC/DCVC-FM 中综合最优——相对 AOM AVM 节省 **16.1%**、相对 DCVC-FM 节省 **11.0%**（PSNR、低时延、YCbCr 4:2:0、MPEG+AOM CTC 序列并用以保证公平）；DCVC 系神经编码器在大背景运动内容上性能不一致 [paper:arxiv:2408.05042]。
- G-PCC 属性工具持续小幅改进：RAHT 末层残差自适应跳过 + 自适应拉格朗日 RDO，动态点云 BD-rate **Luma −3.50% / Cb −5.56% / Cr −4.18%**（vs G-PCC 参考软件，MPEG CTC）[paper:arxiv:2412.05574]。

### 2025：属性增强滤波、评测数据集、LiDAR 专用路线、5G 实测边界

- 集成式维纳滤波器（系数继承 + 方差点分类 + Morton 码快速最近邻）进入 G-PCC 管线：lossless-geometry-lossy-attributes 下相对 **G-PCC v7.0 rc2（GSO 测试模型）** BD-rate **Luma −6.1% / Cb −7.3% / Cr −8.0%** [paper:arxiv:2503.17467]。
- 第三方 V3C 评测数据集补齐：UVG-VPC 开源，12 序列 × 250 帧 × 25 fps，几何 9–12 bit、8-bit RGB、附法线 [paper:arxiv:2504.05888]。
- LPCM 球坐标预测树 + LSTM 预测/变分半径压缩双模式，在 SemanticKITTI 与 **MPEG 指定 Ford 数据集**上 RD 优于 G-PCC 及其他学习式方法 [paper:arxiv:2505.20059]。
- DASH 低时延交付的网络能力边界（泰国商用网实测）：5G SA 全部场景 **>95%** UHD 片段按时送达；LTE **>20%** 超时；NSA 受底层 LTE 制约存疑 [paper:arxiv:2511.20961]。

### 2026：多层/能效主观评估、FCM、竞争对标、GS 与网格新战场

- 多层编码主观评估方法论输出：遵循 MPEG 多层视频编码测试条件，LCEVC（LTM 8.1）作增强层叠加 HD VVC 基础层，两个工作点增强层码率占比约 **10% / 50%**，DCR、25 人、15 个 SDR/HDR 序列，对比 ML-VVC [paper:arxiv:2601.10448]。
- FCM 编码端改造：包装器感知加权 SSE 的 WA-RDO 使 **HEVC 级联 FCM 在 MPEG 测试条件下追平 VVC 级最优方法**，弥合一代编码器代差 [paper:arxiv:2601.22070]。
- 竞争对标：中国 AVS 已完成**第一代 AVS PCC 标准**，与 G-PCC/V-PCC 作技术与性能对比 [paper:arxiv:2602.08613]。
- **GS 编码标准化启动证据**：ISO/IEC JTC1/SC29/WG7 GS 编码 CTC 文档 N1414（2026-01），视频投影式编码为主流路线 [paper:arxiv:2609.29041 摘录]；配套技术涌现——双阶段 Morton 排序将 3DGS 属性转为强局部相关 2D 特征图，压缩性能与运行效率均优于 PLAS 与 Morton ordering（标准兼容方案）[paper:arxiv:2609.29041]。
- 属性帧间运动估计新高度：基于图的帧间运动估计 + 免插值分数体素细化，有损几何下平均码率节省 **vs G-PCC 55.3% / vs GeS-TM 42.3% / vs V-PCC 16.5%**（MPEG 点云数据集；无损与有损几何均优于三锚点）[paper:arxiv:2607.03576]。
- 网格纹理范式挑战 UV 图集：TexF 表面对齐纹理场 + 3DNTC GPU 常驻神经压缩，在 **MPEG 与 AOM 网格基准**上码流与 GPU 常驻两种压缩的平均 RD 均优于代表性 UV 方法（未给具体数值）[paper:arxiv:2609.23606]。
- VVC 后处理滤波：CASR（LoRA 逐序列过拟合 SR，NNR 压缩信令）相对 **VTM21**：随机访问 Y −10.93% / U −15.39% / V −24.41%，全帧内 Y −13.43% / U −5.75% / V −22.94%（JVET CTC A1/A2 序列）[paper:arxiv:2609.37328]。
- 网格无损压缩：OctMesh 在 **MPEG V-DMC（ISO/IEC 23090-29）** 8 序列 256 帧上以平均 **7.033 bits/face** 无损恢复最细层顶点/边/面，码率较 **V-Mesh 低 12.8%**，支持 9 级渐进细化 [paper:arxiv:2610.04281]。
- 5G FWA 场景 OTT 交付：MPEG-DASH 4K，MIMO 持续优于 SISO，5 并发用户下 MIMO+256-QAM 的 VMAF 保持视觉无损阈值以上 [paper:arxiv:2609.25423]。

## 当前状态与关注点

**活跃度**

- 窗口内条目流连续无断档；2026 年（1–10 月）9 条为最密集年度，其中 2026-09 单月 4 条（网格纹理、3DGS、VVC 后处理、5G FWA），与 GS 编码标准化启动（CTC N1414，2026-01）时点吻合，提示体积媒体新表征压缩进入研究热点窗口。〔档案推断〕
- 文献锚点侧记的标准平台版本演进链：G-PCC 参考软件 → G-PCCv20（2022）→ GSO 测试模型 v7.0 rc2（2025）；VTM → VTM21；另有 TMIV、GeS-TM、V-Mesh、LTM 8.1 各就其位。

**开放问题**

1. **学习式增益 vs 标准吸收速度的剪刀差**：学习式方案对 G-PCC/V-PCC 锚点报告数十百分点级增益（>88% [paper:arxiv:2207.12554]、55.3% [paper:arxiv:2607.03576]、10%–35% [paper:arxiv:2202.06028]），而标准侧传统工具改进幅度为个位数百分点（2.1% [paper:arxiv:2106.12236]、3.5–5.6% [paper:arxiv:2412.05574]、6.1–8.0% [paper:arxiv:2503.17467]）；学习工具是否/如何进入标准码流，档案内无证据。〔档案推断〕
2. 神经视频编码器在低时延、大背景运动内容上稳定性不足 [paper:arxiv:2408.05042]。
3. 跨标准**主观**感知对比稀缺：MPEG vs JPEG Pleno 主观对比 2024 年才首次出现 [paper:arxiv:2402.04760]；AVS PCC 对比尚无主观维度证据 [paper:arxiv:2602.08613]。
4. 多标准竞争格局并行：JPEG Pleno 点云 [paper:arxiv:2208.02716]、AOM（AVM 视频 [paper:arxiv:2408.05042]、网格编码 [paper:arxiv:2609.23606]）、AVS PCC [paper:arxiv:2602.08613]。
5. 遗留技术问题：点云几何+颜色联合编解码的质量饱和效应"有待解决" [paper:arxiv:2208.02716]；FCM 级联结构中 SSE-RDO 不感知后处理包装器致比特浪费 [paper:arxiv:2601.22070]；网格纹理 UV 图集范式的 chart 边界结构性损耗 [paper:arxiv:2609.23606]；GS 投影式编码有效性高度依赖投影空间相关性 [paper:arxiv:2609.29041]。
6. DASH 低时延交付强依赖网络制式：SA 5G 可行、LTE 不可行、NSA 存疑 [paper:arxiv:2511.20961]；FWA 场景对 MIMO/调制/用户负载敏感 [paper:arxiv:2609.25423]。

**生态位**

- **事实评测基础设施提供者**：MPEG CTC、MPEG PCC 数据集（MPEG 8i、MVUB、Ford 等）与参考软件（VTM/TMVC 链、TMIV、TMC13、V-Mesh）是跨阵营对比的共同基准——竞争阵营论文亦并用 MPEG 与 AOM CTC 序列以保证公平 [paper:arxiv:2408.05042]，第三方以 V3C 为目标构建开放数据集 [paper:arxiv:2504.05888]。
- **协作与竞争并存**：Green-MPEG 经 JVET 提案在 VTM 落地 [standard_proposal:jvet:m190-Z0046][standard_proposal:jvet:m192-AB0072]；同时对 JPEG/AOM/AVS 存在直接标准级竞争。
- **标准族纵向广度**：档案证据覆盖 2D 视频（VVC/多层/Green-MPEG/能效）、机器视觉（VCM/FCM）、点云（G-PCC/V-PCC/GeS-TM/V3C）、沉浸视频（MIV）、动态网格（V-DMC/V-Mesh）、3DGS（标准化启动期）与传输（DASH），形成"表征—编码—网络交付"全链路生态位。
