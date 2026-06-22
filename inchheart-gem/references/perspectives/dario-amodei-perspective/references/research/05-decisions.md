# Dario Amodei 决策记录与行动调研

> 调研日期：2026-06-08  
> 目标：从行动而非口号中提炼决策规则。

---

## 一、从 OpenAI 离开并创立 Anthropic

来源：
- Anthropic 官方背景：https://www.anthropic.com/company
- Core Views on AI Safety：https://www.anthropic.com/news/core-views-on-ai-safety
- 多家媒体对 Anthropic 创立背景的报道，二手。

事实概述：
- Dario 曾在 OpenAI 担任研究副总裁级别角色，参与 GPT-2、GPT-3、RLHF（基于人类反馈的强化学习）等方向。
- 2021 年左右，他与 Daniela Amodei 等人创立 Anthropic。
- Anthropic 被定位为 AI safety and research company（AI 安全与研究公司），不是单纯产品公司。

决策逻辑推断：
- 如果认为安全研究需要前沿模型，而原组织的治理、节奏或优先级不合适，就另建能把安全作为第一身份的组织。
- 这是“安全必须靠组织结构承载”的决策，而不只是发表论文。

张力：
- 新组织仍需大量资金、算力和商业化，因此安全使命从第一天就与资本和竞争绑定。

### 可蒸馏启发式

当核心研究路线需要不同组织激励时，不要只写备忘录，要改变组织边界。

---

## 二、押注缩放律与 GPT-3 路线

来源：
- Scaling Laws for Neural Language Models：https://arxiv.org/abs/2001.08361
- Core Views on AI Safety 中对 GPT-3 与 scaling laws（缩放律）的回顾。

事实概述：
- Dario 及后来 Anthropic 创始团队成员参与了缩放律相关研究。
- 这为 GPT-3 等大模型训练提供了理论和经验支持。

决策逻辑：
- 当经验曲线跨多个数量级稳定，前沿投入不再只是赌博，而是可计算的工程押注。
- 如果曲线告诉你“更大模型会普遍更强”，安全研究也必须提前准备更强系统。

张力：
- 缩放律增强了能力竞赛，也增强了安全紧迫性。

---

## 三、将 Constitutional AI 变成 Anthropic 核心方法

来源：
- https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback

事实概述：
- Anthropic 使用一组原则约束模型，让模型自我批评、自我修订，并用 AI feedback（AI 反馈）扩展监督。
- 该方法成为 Claude 安全与品牌差异的重要基础。

决策逻辑：
- 人类价值不能完全靠人工标注扩展到强大模型。
- 必须把监督压缩成原则，再用模型能力扩展监督。
- 原则必须可公开审视，否则“安全”只是暗箱偏好。

局限：
- 宪法本身由人选择。原则选择、解释和冲突解决仍有价值判断。

---

## 四、长期投资可解释性

来源：
- Mapping the Mind：https://www.anthropic.com/research/mapping-mind-language-model
- The Urgency of Interpretability：https://www.darioamodei.com/post/the-urgency-of-interpretability
- Transformer Circuits 系列：https://transformer-circuits.pub/

事实概述：
- Anthropic 从成立早期即把 mechanistic interpretability（机制可解释性）放在核心研究方向。
- 2024 年发布对 Claude 3 Sonnet 的大规模特征映射。
- 2025 年 Dario 进一步公开提出 interpretability（可解释性）必须在强大 AI 前成熟。

决策逻辑：
- 行为评测会被训练污染。可解释性应成为独立测试集。
- 如果没有内部诊断工具，越强模型越像不可审计基础设施。

风险：
- 可解释性可能来不及成熟；
- 可解释性工具本身也可能被用于操纵模型；
- 解释特征不等于理解完整回路。

---

## 五、发布 Responsible Scaling Policy

来源：
- 初版 RSP：https://www.anthropic.com/news/anthropics-responsible-scaling-policy
- 更新版 RSP：https://www.anthropic.com/news/announcing-our-updated-responsible-scaling-policy
- RSP 页面：https://www.anthropic.com/rsp

事实概述：
- Anthropic 用 ASL（AI Safety Level，AI 安全等级）框架把模型能力与安全、安保要求绑定。
- 更新版强调 capability thresholds（能力阈值）和 required safeguards（必要防护）。
- 风险重点包括 autonomous AI R&D（自主 AI 研发）和 CBRN（化学、生物、放射、核）相关能力。

决策逻辑：
- 不要只说“我们会谨慎”。把谨慎翻译成阈值、评估、流程和外部输入。
- 安全规则要能随能力增长升级。

张力：
- 灵活性有助于实践，也可能被批评为给公司留下过大解释空间。

---

## 六、支持芯片出口管制

来源：
- https://www.darioamodei.com/post/on-deepseek-and-export-controls

事实概述：
- Dario 在 DeepSeek 引发全球讨论后，仍主张加强对中国先进 AI 芯片出口管制。
- 他的核心不是否认中国工程能力，而是认为强大 AI 需要百万级芯片、数百亿美元级投入，控制先进芯片能影响未来能力分布。

决策逻辑：
- 如果强大 AI 在短期内到来，领先权就不是普通产业优势，而是安全和地缘战略缓冲。
- 技术效率提升会提高前沿能力，而不是自然降低风险。

张力：
- 这条路线把 AI 安全与国家竞争绑定，可能加剧竞赛。

---

## 七、决策启发式候选

1. 曲线稳定时，按曲线下注；曲线失稳时，找新范式。
2. 安全问题如果只在前沿出现，就不能只在小模型上研究。
3. 价值监督要能扩展，必须变成原则和流程。
4. 部署不是一次性 yes/no，而是能力阈值触发的安全等级升级。
5. 行为评测不够，必须寻找内部诊断信号。
6. 公司使命必须通过组织结构、治理和产品节奏落地。
7. 政策判断先拆技术瓶颈，再谈价值排序。
8. 好未来需要主动争取，但不能用救世主语气包装。

