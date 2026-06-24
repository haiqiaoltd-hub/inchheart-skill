# Perspective Intake Prompt

用于 Phase 0A。目标是用最少问题确定蒸馏对象、用途和 preset，不把用户拖进问卷。

## Required Decisions

1. `target_name`: 人名、主题名或模糊需求。
2. `artifact_kind`: `person` / `topic-framework` / `self`。
3. `preset`: 从 `references/perspective-presets.json` 选择一个主 preset。
4. `use_case`: 思维顾问、作品分析、决策参考、创作训练、批评反馈、角色对话。
5. `research_mode`: `web-only` / `local-first` / `local-only`。
6. `depth`: `standard` / `deep`。

## Question Budget

- 用户已经点名且说“就做”：不追问，默认 `person + standard + web-only + 思维顾问`。
- 信息不足但风险低：最多问 1 个问题。
- 同名人物、争议人物、在世人物近期动态、用户提供私有素材：最多问 2 个问题。

## Output

确认后给出：

```text
蒸馏对象：
主 preset：
用途：
调研模式：
深度：
新建/更新：
已知风险：
```
