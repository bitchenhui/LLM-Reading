# 视频/图像压缩前沿论文精读（2026-06）

本目录汇总了 `paper/` 下 6 篇 2026 年 6 月放出的 arXiv 论文的精读笔记，覆盖了当前学习式视频/图像编码研究的几个关键方向：

| # | 论文 | 方向 | 关键词 | 摘要文档 |
| - | ---- | ---- | ------ | -------- |
| 1 | LLM-Driven Heuristic Frame-Level QP Adaptation for VVenC | 传统编码器（VVenC）+ LLM 辅助 | LLM、RDO、帧级 QP 分配、进化搜索 | [01_LLM-VVenC-QP.md](01_LLM-VVenC-QP.md) |
| 2 | Accelerating MMVD via Filter Difference Analysis for VVenC | 传统编码器（VVenC）加速 | MMVD、VVC、快速搜索、滤波器差分 | [02_MMVD-Fast.md](02_MMVD-Fast.md) |
| 3 | MoECodec: Image Compression for Joint Human & Machine Perception via MoE | 学习式图像编码（多任务） | MoE、Expert-Choice Routing、机器视觉 | [03_MoECodec.md](03_MoECodec.md) |
| 4 | ZeroGVC: Zero-Shot Generative Video Compression with AR Diffusion Priors | 生成式视频压缩（免训练） | 扩散、DDCM、自回归、低延迟 | [04_ZeroGVC.md](04_ZeroGVC.md) |
| 5 | MLVC: Multi-platform Learned Video Codec for Real-World Deployment | 学习式视频编码（可部署） | 跨平台一致性、NPU、Scale Sending | [05_MLVC.md](05_MLVC.md) |
| 6 | NVRC++: Enhanced Neural Video Representation Compression | 隐式神经表示（INR）视频压缩 | INR、HiNeRV++、高分辨率 feature grid | [06_NVRC++.md](06_NVRC++.md) |

## 主线视角

这六篇论文形成了一张覆盖压缩全谱系的地图：

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        视频/图像压缩研究谱系                                │
├───────────────────────────┬────────────────────────┬─────────────────────┤
│    传统标准编码器优化       │       学习式编码器      │     生成/表示学习    │
├───────────────────────────┼────────────────────────┼─────────────────────┤
│ ① LLM-VVenC-QP（LLM 生    │ ③ MoECodec（MoE 图像    │ ④ ZeroGVC（免训练   │
│    成 RDO 启发式）         │    编码 + 多任务）      │    扩散视频编码）    │
│ ② MMVD-Fast（VVenC MMVD   │ ⑤ MLVC（跨平台可部署    │ ⑥ NVRC++（INR 视频  │
│    快速搜索）              │    NPU 编码器）         │    编码，多复杂度）  │
└───────────────────────────┴────────────────────────┴─────────────────────┘
```

- **传统标准侧**（① ②）在 VVenC 上做的优化，一个用 LLM 自动发现帧级 QP 决策规则，一个用信号分析加速 MMVD 搜索，代表"如何让 VVC 更快、更准"。
- **学习式编码器侧**（③ ⑤）关心多任务 / 部署两大瓶颈：MoECodec 用 MoE 让一个模型服务多种下游视觉任务；MLVC 直面 NPU 跨平台一致性问题，首次让端到端神经视频编码在多家硬件上稳定运行。
- **生成 / 表示学习侧**（④ ⑥）用生成先验或隐式表示彻底改写压缩范式：ZeroGVC 不训练直接复用视频扩散模型；NVRC++ 把视频压成一个 INR + 高分辨率 feature grid。

## 每篇一句话

1. **LLM-VVenC-QP**：用 DeepSeek 迭代进化 Python 启发式函数，为 VVenC 每一帧从 5 个候选 QP 中挑一个，最终自动发现"熵约束 RDO"启发式，在 CTC/UVG/MCL-JCV 上比固定 QP 平均省 1.26% 码率。
2. **MMVD-Fast**：把 VVC 8-tap 分数插值近似为 2-tap，得到只需一次内积就能判断 MMVD 候选是否值得计算的准则，把 MMVD 搜索比从 21% 降到 11%，η 从 11.79 降到 7.10。
3. **MoECodec**：把 transformer LIC 里的 FFN 换成 token 级 MoE，用 Expert-Choice Routing + 空间 TV 正则 + Group-Shuffle MLP 解决路由散乱和参数膨胀，重建 BD-Rate 提升 6–12%，下游任务再提 8–10%。
4. **ZeroGVC**：GOP 首帧用图像编码器，P 帧只传"少量码本噪声原子的索引 + 系数"来引导预训练自回归视频扩散模型的少步一致性采样，完全免训练地实现低延迟生成式视频压缩。
5. **MLVC**：把 DCVC-RT 的 scale 参数显式通过 hyperprior 传输，避免 NPU 跨平台熵解码崩溃；配合 Gated Memory / ReGLU / LTR 恢复码率损失，第一次在 Apple/Intel/Qualcomm NPU 上以 100 FPS 稳定跑通神经视频编码，MOS 上超 HEVC-QSV 70%+。
6. **NVRC++**：轻量 HiNeRV++ 网络 + 多个高分辨率 feature grid，把复杂度与质量解耦。四档复杂度（7k–360k MACs/pixel）单模型跨全码率区间，S3 变体在 UVG 上比 SOTA INR 编码器 NVRC 解码快 7.6 倍，性能相当。

## 阅读建议

- 关注 **VVenC 优化** → 从 ①、② 入手，了解在标准编码器上做 fast/RDO 改进的两种典型思路。
- 关注 **神经编码器 deployable / real-time** → 直接看 ⑤ MLVC 与 ⑥ NVRC++。
- 关注 **AI-for-Codec 与生成式压缩** → 看 ① LLM 用法 与 ④ ZeroGVC 的免训练框架。
- 关注 **面向机器视觉/多任务** → ③ MoECodec 是本轮唯一一篇。
