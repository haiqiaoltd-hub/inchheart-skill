# Perspective Analyzer Prompt

用于 Phase 2。把调研材料提炼为可运行的认知结构。

不要优化“像不像本人说话”的表演感。优先提取 HOW they think，而不是 WHAT they said。

## Extraction Targets

### 0. Soul Kernel

先读取 `references/soul-kernel-framework.md`，提炼人物的动力层。不要把它写成道德评价，也不要写成漂亮标签。

输出四项：

```text
Default Loop / 不得不:
  - Action:
  - Evidence anchors:
  - Confidence:

Asymmetric Sacrifice / 愿意为了什么而输:
  - Protects:
  - Sacrifices:
  - Evidence anchors:
  - Confidence:

Core Paradox / 核心矛盾:
  - Pole A:
  - Pole B:
  - Trigger conditions:
  - Evidence anchors:

Information Filter / 选择性失明:
  - Highlight signals:
  - Background noise:
  - Blind spot:
  - Evidence anchors:
```

这些字段是后续心智模型、决策启发式和 Agentic Protocol 的动力来源。证据不足时标为低置信度，不要编造。

### 1. Mental Models

每个候选模型必须通过三重门：

| Gate | 问题 |
|---|---|
| Cross-context recurrence | 是否至少跨 2 个不同语境反复出现？ |
| Generative power | 是否能预测他面对新问题会先看什么？ |
| Exclusivity | 是否明显区别于普通聪明人的常识？ |

通过 3 门：保留为核心心智模型。  
通过 1-2 门：降级为决策启发式。  
通过 0 门：丢弃。

每个模型输出：

```text
Name:
Definition:
Sees first:
Filters out:
Evidence anchors:
Application:
Failure mode:
Gates passed:
```

### 2. Decision Heuristics

提取 5-10 条“如果 X，则 Y”的判断规则。每条必须有场景或案例。

### 3. Expression DNA

根据 preset 调整表达维度：

- 思想家：概念密度、论敌构造、抽象阶梯、反讽/断裂。
- 文学家：叙述距离、意象群、节奏、沉默和省略。
- 艺术家：视觉/材料词汇、形式判断、空间隐喻。
- 导演：镜头、时长、声音、剪辑、观看位置。
- 企业家：数字、客户、组织、激励、简化。
- 科学家：定义、实验、证明、误差、类比纪律。
- 宗教人物：寓言、律令、修行步骤、沉默。
- 政治人物：敌我、组织、历史类比、动员语言。

### 4. Tensions

至少保留 2 个张力。不要为了一致性抹平矛盾。张力分为：

- temporal: 观点随时间演化。
- contextual: 不同领域采用不同原则。
- inherent: 价值本身互相拉扯。

### 5. Intellectual Genealogy

提取：

- influenced by
- diverged from
- influenced
- tradition or anti-tradition

### 6. Agentic Protocol Seeds

从心智模型反推出此人遇到新问题会先调查的维度。输出 3-5 个研究维度，不要写通用“查资料”。

Agentic Protocol 必须显式使用 Soul Kernel：

- 用 `Information Filter` 决定先看什么、忽略什么。
- 用 `Default Loop` 决定默认动作。
- 用 `Asymmetric Sacrifice` 处理两难代价。
- 用 `Core Paradox` 保留冲突，不把视角磨平。

## Output

输出结构化分析，不写最终卡片正文。每条推断必须能回到 evidence anchors。
