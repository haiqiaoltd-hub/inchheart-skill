# Professor Card Schema

每张当前核心教授卡必须满足：

| Section | 作用 |
|---|---|
| `## 任务` | 定义这位教授解决什么类型的问题 |
| `## 工作协议` | 给出处理问题的步骤 |
| `## 证据抓手` | 说明不同问题类型应抓哪些证据 |

约束：

- 当前主入口只允许 15 张 `references/professors/<id>/PROFESSOR.md`。
- 旧 16 教授不得出现在当前主路由 `core_professors` 中。
- 不允许引用已删除的旧教授或旧细分 references。
- 审计分析必须优先读取 `/Users/mac/Repository/Projects/InchHeart Skill/inchheart-analysis/SKILL.md` 和 `/Users/mac/Repository/Projects/InchHeart Skill/inchheart-analysis/references/audit-model.md`，不得作为教授卡出现。
- `references/methods/audit-response-protocol.md` 和 `references/methods/dimensional-audit.md` 只是同步镜像/回退，不得作为教授卡出现。
- 不允许把人物 perspective、酒馆或人物蒸馏流程放入本技能。
