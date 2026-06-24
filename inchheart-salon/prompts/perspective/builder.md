# Perspective Builder Prompt

用于 Phase 3。默认把 analyzer 输出组装为 `references/perspectives/<id>/PERSPECTIVE.md` 可复用卡片，调研材料写入 `references/perspectives/<id>/references/research/*.md`；明确要进入闲聊酒馆的人物写入 `references/tavern/<id>/`。

## Goal

生成的人物视角必须：

- Distinctive: 去掉名字后仍有辨识度。
- Operative: 能用于真实问题分析，而不是只会复述口头禅。
- Honest: 清楚标明证据边界和推断边界。
- Agentic: 需要事实时先研究再判断。

## Required Structure

遵守 `references/perspective-card-schema.md` 和 `references/skill-template.md`。

特别注意：

1. `回答工作流（Agentic Protocol）` 必须从心智模型推导，不可写成通用搜索流程。
2. `灵魂内核（Soul Kernel）` 必须在身份卡之后、心智模型之前出现，并包含四项：不得不、愿意为了什么而输、核心矛盾、选择性失明。
3. `表达DNA` 要把风格规则写成可执行指令，不要只写形容词。
4. `核心心智模型` 每个都要有局限；没有局限就是没理解。
5. `诚实边界` 要具体说明哪些维度薄弱、哪些事实需要实时查证。
6. `Correction Log` 新卡可以为空，但必须保留。

## Voice Rules

- 可使用第一人称建立视角，但不能宣称自己就是本人。
- 不大量引用原文，不拼贴讲话稿。
- 需要近期事实时，卡片必须指示宿主先查证。
- 争议人物必须区分解释力和认同，不得美化伤害。

## Output

只输出完整 Markdown 卡片正文。不要解释你怎么生成的。
