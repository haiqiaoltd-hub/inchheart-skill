# CLI 模型参数配置(自建中转)

给各 CLI 配置「自建中转站」(`api.eastart.asia/v1`,即 `ju-zen` / `ju-nvidia-nim` 渠道)上的模型参数——上下文上限、推理(reasoning)、模态(modalities)、输出上限。

核心事实:**每个 CLI 的配置模型完全不同,字段名和生效范围都不一样,不能互相照抄。** 自建中转的模型是自定义短名,不在 models.dev 标准库里,所以元信息基本都要手写,CLI 不会自动补全。

## 通用判断流程

1. 先定位该 CLI 的配置文件(见下表)。
2. 读它的源码 / schema 确认字段名,不要凭记忆写。
3. 改完用 `jq empty`(JSON)或 `yq eval '.'`(YAML)校验语法。
4. 改前先备份:`cp <config> <config>.bak.$(date +%Y%m%d_%H%M%S)`。
5. 重启该 CLI 让配置重新加载。

## OpenCode

| 项 | 值 |
|---|---|
| 配置文件 | `~/.config/opencode/opencode.json`(JSON) |
| 模型数据源 | 远程 `https://console.opencode.ai/api/config`(需登录)+ 公开 `https://models.dev/api.json` |
| 结构 | `provider.<id>.models.<model>` 逐个模型配完整元信息 |

模型对象支持的键(与 `name` 平级,来自源码 `packages/core/src/models-dev.ts` 的 `Model` schema):

- `attachment`: bool —— 是否支持附件
- `reasoning`: bool —— **支持推理就设 true,面板才显示推理档位菜单**
- `temperature`: bool
- `tool_call`: bool —— 工具调用
- `limit`: `{ context, input, output }` —— 上下文 / 输入 / 输出上限(整数 token)
- `modalities`: `{ input, output }` —— 合法值 `text / audio / image / video / pdf`
- `cost`: `{ input, output, cache_read, cache_write }`
- `options`: provider 选项(见下)

关键事实:
- **不要在 config 里写死 `options.reasoningEffort`。** 官方 5 个免费模型的 `options` 都是 `null`,推理档位(默认/Low/Medium/High/Max)由 `reasoning: true` 触发、运行时 UI 里选。写死会锁档,也可能触发 schema 校验问题。
- 档位菜单对所有 `reasoning: true` 的模型是同一套,OpenCode **无法**在 config 里限制「某模型只显示 2 档/3 档」。某档是否生效取决于上游认不认 `reasoning_effort`。
- `npm: "@ai-sdk/openai-compatible"` 这条链路:`reasoningEffort` 会被 lowerer(`packages/core/src/v1/config/provider-options.ts`)重命名为 `reasoning_effort` 透传。原生 `@ai-sdk/openai` 才会过滤掉 `max`;openai-compatible 不过滤。
- 取官方权威数值:`curl -sS https://models.dev/api.json | jq '.opencode.models["deepseek-v4-flash"]'`。

## Hermes

| 项 | 值 |
|---|---|
| 配置文件 | `~/.hermes/config.yaml`(YAML) |
| 模型数据源 | 内置 `agent/model_metadata.py` 的 `DEFAULT_CONTEXT_LENGTHS` 表 + `models_dev_cache.json` + 探测 |
| 结构 | 顶层 `model:` 单默认模型 + `custom_providers[]` 逐 provider/模型 |

两个层级,职责不同:

1. **顶层 `model:` 段** —— 只对「当前默认模型」生效。合法键:`default`、`provider`、`base_url`、`api_key`、`api_mode`、`supports_vision`、`max_output_tokens`、`context_length`、`max_tokens`。`context_length` 是最高优先级覆盖(`agent_init.py` 读 `_model_cfg.get("context_length")`)。
2. **`custom_providers[]`** —— 逐 provider 登记,`/model` 切换时复用。provider 级键:`name / base_url / api_key / key_env / api_mode / model(默认) / models / context_length / discover_models / extra_body`。

关键事实:
- **`custom_providers[].models.<model>` 这一层只读 `context_length` 一个键**(`hermes_cli/config.py` 的 `get_custom_provider_context_length` 是唯一真相来源)。不支持 per-model 的 reasoning / modalities / max_output_tokens。
- 上下文解析优先级(`get_model_context_length`):① `model.context_length` 显式覆盖 → ② `custom_providers` per-model → ③ 缓存/探测 → ④ `DEFAULT_CONTEXT_LENGTHS` 内置表(**子串匹配**,longest-key-first)→ ⑨ fallback **256K**。
- **子串匹配是坑**:`nemotron-3-ultra-550b-a55b` 会命中内置 `"nemotron": 131072` 被砍成 128K。必须在 `custom_providers` per-model 显式写 `context_length` 覆盖。
- 输出上限 / 视觉 / 推理只在顶层 `model:` 段对当前默认模型生效,切到别的模型仍走默认那套——这是架构限制,不是配置遗漏。
- 查内置表是否认得某模型:`grep -E '"<model>"' ~/.hermes/hermes-agent/agent/model_metadata.py`。

## 两套对照速记

| 能力 | OpenCode | Hermes |
|---|---|---|
| 逐模型上下文 | `models.<m>.limit.context` | `custom_providers[].models.<m>.context_length` |
| 逐模型推理 | `models.<m>.reasoning: true` | 不支持(只顶层默认模型) |
| 逐模型模态 | `models.<m>.modalities` | 不支持 |
| 输出上限 | `models.<m>.limit.output` | 顶层 `model.max_output_tokens`(仅默认) |
| 推理档默认值 | 不写(交运行时 UI) | 顶层 `model` / `agent.reasoning_effort` |
| 校验命令 | `jq empty <file>` | `yq eval '.' <file>` |

## 当前自建中转的模型规格(2026-06 实配)

`ju-zen` 渠道(`api.eastart.asia/v1`):

| 模型 | context | output | reasoning | modalities |
|---|---|---|---|---|
| big-pickle | 200K | 32K | 是 | text |
| deepseek-v4-flash | 1M | 384K | 是 | text |
| mimo-v2.5 | 1M | 32K | 是 | text+image+audio+video |
| nemotron-3-ultra-550b-a55b | 1M | 32K | 是 | text |
| north-mini-code | 256K | 32K | 是 | text |

`ju-nvidia-nim` 渠道是英伟达上游,推理代码未知,不擅自配推理参数。

服务器侧反代(`zen-proxy.py` 等)只做模型名映射 + 原样透传 body,不改 `reasoning_effort` 等字段。推理等级在 CLI 设、反代透传、上游决定是否生效。详见 `inchheart-cloud` 技能。
