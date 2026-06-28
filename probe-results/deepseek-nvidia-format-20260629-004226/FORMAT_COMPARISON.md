# DeepSeek 官方 vs NVIDIA NIM DeepSeek 响应格式对比

测试时间：2026-06-29 00:42 本地时间附近  
测试请求：`请只回复两个字：通过`，`temperature=0`，`max_tokens=64`

## 文件位置

| 内容 | 路径 |
|---|---|
| 测试脚本 | `scripts/probe_deepseek_nvidia_formats.py` |
| 本次结果根目录 | `probe-results/deepseek-nvidia-format-20260629-004226` |
| 汇总 JSON | `probe-results/deepseek-nvidia-format-20260629-004226/summary.json` |
| 官方 flash 原始非流式 | `deepseek-official/deepseek-v4-flash/nonstream.raw` |
| 官方 flash 原始流式 | `deepseek-official/deepseek-v4-flash/stream.raw.sse` |
| 官方 pro 原始非流式 | `deepseek-official/deepseek-v4-pro/nonstream.raw` |
| 官方 pro 原始流式 | `deepseek-official/deepseek-v4-pro/stream.raw.sse` |
| NVIDIA flash 原始非流式 | `nvidia-nim/deepseek-ai__deepseek-v4-flash/nonstream.raw` |
| NVIDIA flash 流式超时记录 | `nvidia-nim/deepseek-ai__deepseek-v4-flash/stream.raw.sse` |
| NVIDIA pro 非流式超时记录 | `nvidia-nim/deepseek-ai__deepseek-v4-pro/nonstream.raw` |
| NVIDIA pro 流式超时记录 | `nvidia-nim/deepseek-ai__deepseek-v4-pro/stream.raw.sse` |

## 可用性结果

| Provider | Model | 非流式 | 流式 | 耗时/现象 |
|---|---|---:|---:|---|
| DeepSeek 官方 | `deepseek-v4-flash` | 200 | 200 | 非流式约 0.9s，流式约 0.8s |
| DeepSeek 官方 | `deepseek-v4-pro` | 200 | 200 | 非流式约 1.1s，流式约 1.3s |
| NVIDIA NIM | `deepseek-ai/deepseek-v4-flash` | 200 | 超时 | 非流式约 20s；流式 45s 读超时 |
| NVIDIA NIM | `deepseek-ai/deepseek-v4-pro` | 超时 | 超时 | 非流式和流式均 45s 读超时 |

补充：上一轮测试中，NVIDIA `deepseek-ai/deepseek-v4-flash` 流式成功过一次，耗时约 13.4s；该成功样本保存在 `probe-results/deepseek-nvidia-format-20260629-003909/nvidia-nim/deepseek-ai__deepseek-v4-flash/stream.raw.sse`。

## 非流式格式差异

| 字段 | DeepSeek 官方 | NVIDIA NIM |
|---|---|---|
| 顶层字段 | `choices`, `created`, `id`, `model`, `object`, `system_fingerprint`, `usage` | `choices`, `created`, `id`, `metadata`, `model`, `object`, `usage` |
| `system_fingerprint` | 有 | 无 |
| `metadata` | 无 | 有，例如 `{"weight_version":"default"}` |
| `choices[0]` 额外字段 | 无 `matched_stop` | 有 `matched_stop` |
| `message.tool_calls` | 字段不存在 | 字段存在，值为 `null` |
| `message.reasoning_content` | 字段存在，通常为字符串 | 字段存在，但本次 flash 为 `null` |
| `usage.prompt_tokens_details` | 对象，例如 `{"cached_tokens":0}` | `null` |
| `usage.completion_tokens_details` | 对象，含 `reasoning_tokens` | 字段不存在 |
| `usage.reasoning_tokens` | 不在顶层 usage | NVIDIA 放在 usage 顶层 |
| 缓存字段 | `prompt_cache_hit_tokens`, `prompt_cache_miss_tokens` | 无 |

关键兼容点：

1. NVIDIA 非流式会返回 `message.tool_calls: null`，客户端或代理不应假设它是数组。
2. NVIDIA 非流式会返回 `message.reasoning_content: null`，不能直接当字符串拼接。
3. 官方 DeepSeek 的 reasoning 是正常字符串，并且 completion token 里包含 reasoning 统计。

## 流式格式差异

### DeepSeek 官方

官方两个模型流式结构稳定：

| 特征 | 结果 |
|---|---|
| 每个 SSE JSON 顶层 | `choices`, `created`, `id`, `model`, `object`, `system_fingerprint`, `usage` |
| 空 `choices: []` | 没有 |
| usage | 最后一个带正常 `choices` 的 chunk 同时带 `usage` |
| `delta.content` | reasoning 阶段为 `null`；最终内容 chunk 为 `"通过"`；finish chunk 为 `""` |
| `delta.reasoning_content` | reasoning 阶段为字符串增量；最终内容/finish 阶段为 `null` |
| `delta.tool_calls` | 无 |
| 增量类型 | 正常增量，不是累计全文 |

官方样本中的典型 chunk：

```json
{"delta":{"content":null,"reasoning_content":"我们"}}
{"delta":{"content":"通过","reasoning_content":null}}
{"delta":{"content":"","reasoning_content":null},"finish_reason":"stop","usage":{...}}
```

### NVIDIA NIM flash 成功样本

NVIDIA `deepseek-ai/deepseek-v4-flash` 流式成功样本结构：

| 特征 | 结果 |
|---|---|
| 每个 SSE JSON 顶层 | `choices`, `created`, `id`, `model`, `object`, `usage` |
| 空 `choices: []` | 有，最后 usage-only chunk |
| usage | 单独一个 `choices: []` chunk 承载 usage |
| `delta.content` | 初始为 `""`，内容 chunk 为 `"通过"`，finish chunk 为 `null` |
| `delta.reasoning_content` | 全程 `null` |
| `delta.tool_calls` | 字段存在，值为 `null` |
| `matched_stop` | 每个 choice 上都有，finish chunk 为 `1` |
| 增量类型 | 本次不是累计全文 |

NVIDIA 成功样本中的典型 chunk：

```json
{"delta":{"role":"assistant","content":"","reasoning_content":null,"tool_calls":null},"finish_reason":null}
{"delta":{"role":null,"content":"通过","reasoning_content":null,"tool_calls":null},"finish_reason":null}
{"delta":{"role":null,"content":null,"reasoning_content":null,"tool_calls":null},"finish_reason":"stop","matched_stop":1}
{"choices":[],"usage":{"prompt_tokens":22,"total_tokens":24,"completion_tokens":2,"prompt_tokens_details":null,"reasoning_tokens":0}}
```

## 兼容性判断

当前 NVIDIA NIM DeepSeek 与官方 DeepSeek 的主要不兼容点不是模型名，而是响应 shape：

| 问题 | 影响 |
|---|---|
| NVIDIA 流式最后追加 `choices: []` usage chunk | Copilot/部分 OpenAI 客户端可能报 `Response contained no choices` |
| NVIDIA 在 `delta` 里保留 `tool_calls: null` | 客户端如果假设 `tool_calls` 存在就必须是数组，可能报错 |
| NVIDIA 在 `message` 里保留 `tool_calls: null` | 非流式转换时也要清理或归一化 |
| NVIDIA `reasoning_content` 常为 `null` | 不能按字符串处理；需要跳过或归一为空字符串 |
| NVIDIA usage schema 与官方不同 | New API/计费/缓存统计不能照搬官方 DeepSeek 字段 |
| NVIDIA `deepseek-v4-pro` 本次不可稳定返回 | 这是可用性问题，不能只靠格式修复解决 |

## 建议的代理归一化规则

1. 对流式 chunk：
   - 如果 `choices` 是空数组，并且只有 `usage`，默认不要转发给 Copilot 类客户端。
   - 保留给需要 usage 的 OpenAI 客户端时，应该做客户端/渠道开关。
2. 对每个 `choice.delta`：
   - 删除值为 `null` 的 `tool_calls`。
   - 删除值为 `null` 的 `reasoning_content`。
   - 删除值为 `null` 的 `content`；但保留 `content: ""` 只在需要严格复刻上游时使用。
3. 对非流式 `message`：
   - 删除 `tool_calls: null`。
   - 删除或归一化 `reasoning_content: null`。
4. 对 usage：
   - 允许 `prompt_tokens_details` 为 `null`。
   - 同时兼容官方的 `completion_tokens_details.reasoning_tokens` 和 NVIDIA 的顶层 `usage.reasoning_tokens`。
5. 对错误/超时：
   - NVIDIA `deepseek-v4-pro` 应被标记为上游不稳定，代理层不能把超时伪装成正常空 choices。

