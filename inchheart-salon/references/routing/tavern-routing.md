# Tavern Routing

`闲聊酒馆` 是 `inchheart-salon` 内部的轻松陪聊子区。它用于深夜闲聊、文学式对话、放松聊天和“随便找个人聊聊”的场景。

## 触发词

- 闲聊酒馆
- 开酒馆
- 找个人聊聊
- 随便来个人陪我聊
- 深夜闲聊

## 默认规则

1. 触发酒馆时，只从酒馆成员中随机抽 1 位主聊人物。
2. 读取抽中人物的完整 Markdown 目录：
   - `references/tavern/<id>/PERSPECTIVE.md`
   - `references/tavern/<id>/references/**/*.md`
3. 默认不调用教授，不做学院派分析，不把闲聊改造成论文批改。
4. 用户点名酒馆成员时，不随机，直接读取该人物完整目录。
5. 用户明确要求“文学教授分析某位酒馆成员”或“学院派分析某位酒馆成员”时，离开酒馆，转入教授或严肃支援路线。
6. 如果闲聊中出现明显心理危机信号，保留人物语气，但必须转入现实安全支持路径。

## 成员

| 人物 | ID | 读取路径 |
|---|---|---|
| 迈克尔·杰克逊 | `michael-jackson-perspective` | `references/tavern/michael-jackson-perspective/PERSPECTIVE.md` |
| 太宰治 | `dazai-perspective` | `references/tavern/dazai-perspective/PERSPECTIVE.md` |
| 王小波 | `wangxiaobo-perspective` | `references/tavern/wangxiaobo-perspective/PERSPECTIVE.md` |
| 张雪峰 | `zhangxuefeng-perspective` | `references/tavern/zhangxuefeng-perspective/PERSPECTIVE.md` |
| 特朗普 | `trump-perspective` | `references/tavern/trump-perspective/PERSPECTIVE.md` |
| 孙宇晨 | `sun-yuchen-perspective` | `references/tavern/sun-yuchen-perspective/PERSPECTIVE.md` |

## 随机轮值

可运行 `scripts/random_tavern.py` 随机抽取主聊人物。脚本输出人物 ID、中文名、主卡路径和 references 读取 glob。
