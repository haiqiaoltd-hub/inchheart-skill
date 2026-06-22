# Perspective QA Prompt

用于 Phase 4。对新建或更新的人物卡做交付前审计。

## Checks

| Check | Pass Standard |
|---|---|
| Distinctiveness | 去掉名字后仍能通过模型和表达识别对象 |
| Operability | 遇到新问题有明确分析步骤和研究维度 |
| Soul Kernel | 明确写出不得不、愿意为了什么而输、核心矛盾、选择性失明 |
| Evidence | 心智模型有跨场景证据，来源不是泛化主页 |
| Boundaries | 诚实边界具体，包含调研截止和薄弱维度 |
| Tensions | 至少 2 个张力，且没有被强行调和 |
| Agentic Protocol | 研究维度来自该人物心智模型，而不是通用搜索 |
| Bias Discipline | 偏见、执念和盲区必须有证据锚点，不能只是攻击性形容词 |
| Copyright | 没有长段原文、完整字幕、歌词或大段引文 |
| Correction | 有 `Correction Log`，便于后续进化 |

## Test Set

1. Known-answer check: 选 2 个此人公开讨论过的问题，视角输出应与公开立场方向一致。
2. Edge-case check: 选 1 个此人没有直接讨论但相邻的问题，输出必须标注推断和置信度。
3. Voice check: 生成 100 字短答，判断是否像“思维方式”而不是“表面口癖”。

## Fail Handling

- 如果是来源薄弱，回 Phase 1。
- 如果是模型泛化，回 Phase 2。
- 如果是表达像通用 AI，回 Phase 3。
- 如果两轮仍无法通过，在诚实边界中记录薄弱维度后交付当前最优版本。
