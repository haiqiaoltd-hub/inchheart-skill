---
name: inchheart-litellm-explain
description: Use for Wang Donghong's local LiteLLM proxy that adapts VS Code Copilot, Claude, and custom model providers, including NVIDIA Build/NIM multi-account routing, OpenAI Compatibility Responses endpoints, chatLanguageModels.json, compatibility callbacks, tool schema sanitizing, output-token budgets, redacted request metrics, slow-request statistics, model health probing, health panel, 429/cooldown handling, previous_response_id errors, ToolDescription errors, and related Obsidian notes.
---

# InchHeart LiteLLM Explain

## Scope

Use this skill to inspect, explain, repair, or extend Heart's local LiteLLM gateway for Copilot, Claude, and other custom model providers.

Primary local files:

| File | Purpose |
| --- | --- |
| `/Users/mac/litellm_config.yaml` | LiteLLM model list, provider endpoints, environment variable names, router settings |
| `/Users/mac/start-litellm-nvidia.sh` | LaunchAgent start script; loads provider keys from YAML into environment |
| `/Users/mac/copilot_compat_callbacks.py` | Copilot compatibility callback |
| `/Users/mac/Library/LaunchAgents/com.inchheart.litellm-nvidia.plist` | LaunchAgent service |
| `/Users/mac/Library/Application Support/Code/User/chatLanguageModels.json` | VS Code Copilot custom model definitions |
| `/Users/mac/litellm.log`, `/Users/mac/litellm.err.log` | Runtime logs |
| `/Users/mac/litellm_request_metrics.jsonl` | Redacted request metrics written by the callback |
| `/Users/mac/litellm_slow_requests.jsonl` | Slow requests and failures |
| `/Users/mac/litellm_health_probes.jsonl` | Active model health probe results |
| `/Users/mac/bin/litellm-health-panel` | Local health panel service on `http://127.0.0.1:8787` |
| `/Users/mac/bin/litellm-health-probe` | Manual health probe CLI |
| `/Users/mac/Library/LaunchAgents/com.inchheart.litellm-health-panel.plist` | Health panel LaunchAgent |

Do not print or write API key values into chat summaries, Obsidian notes, or skill files. Local service config may contain keys when the user explicitly provides them.

## Decision Tree

1. Identify the API surface first:

| User/provider case | Keep VS Code `apiType` | Local URL |
| --- | --- | --- |
| NVIDIA Build / NIM OpenAI-compatible chat endpoint | `chat-completions` | `http://127.0.0.1:4000/v1/chat/completions` |
| OpenAI Compatibility provider with complete Responses support | `responses` | `http://127.0.0.1:4000/v1` |
| OpenAI Compatibility provider that rejects `previous_response_id` but supports chat | `chat-completions` | `http://127.0.0.1:4000/v1/chat/completions` |
| Other OpenAI-compatible chat provider | `chat-completions` unless proven otherwise | Usually `http://127.0.0.1:4000/v1/chat/completions` |

2. Match the fix to the error:

| Error / symptom | Likely fix |
| --- | --- |
| `Response too long` | Ensure callback is loaded; review finish_reason and output budget logic |
| `ToolDescription description ... NoneType` | Tool schema sanitizer must run before upstream |
| `Unsupported parameter: previous_response_id` | Test direct upstream Responses with a real response id; if it still fails and chat works, switch that provider to `chat-completions` |
| `401 Invalid token` | Verify provider-specific environment variable was loaded by start script |
| NVIDIA `429` | Use multi-key model groups, cooldown, and optional per-deployment `rpm` |
| Streaming timeout / `MidStreamFallbackError` | Lower per-model output budget or avoid that model for Agent workflows |

3. Load the relevant reference:

| Task | Read |
| --- | --- |
| Inspect current service/files | `references/local-files.md` |
| NVIDIA multi-account routing | `references/nvidia-routing.md` |
| Add or repair non-NVIDIA provider / changing endpoint | `references/openai-compatibility.md` |
| Change callback behavior | `references/copilot-callback.md` |
| Diagnose errors | `references/troubleshooting.md` |
| Inspect redacted logs, slow requests, or model health panel | `references/observability.md` |

## Workflow

1. Back up files before editing:

```bash
ts="$(date +%Y%m%d-%H%M%S)"
cp /Users/mac/litellm_config.yaml "/Users/mac/litellm_config.yaml.bak.$ts"
cp /Users/mac/copilot_compat_callbacks.py "/Users/mac/copilot_compat_callbacks.py.bak.$ts"
cp /Users/mac/start-litellm-nvidia.sh "/Users/mac/start-litellm-nvidia.sh.bak.$ts"
cp "/Users/mac/Library/Application Support/Code/User/chatLanguageModels.json" \
  "/Users/mac/Library/Application Support/Code/User/chatLanguageModels.json.bak.$ts"
```

2. Inspect without leaking secrets:

```bash
launchctl print "gui/$(id -u)/com.inchheart.litellm-nvidia" | rg "state =|pid =|last exit code"
curl -sS http://127.0.0.1:4000/v1/models | jq '{count:(.data|length), models:[.data[].id]}'
rg -n "routing_strategy|callbacks|model_name:|api_base:|api_key: os.environ" /Users/mac/litellm_config.yaml
rg -n "Response too long|ToolDescription|previous_response_id|429|Invalid token|MidStreamFallback|Timeout" \
  /Users/mac/litellm.err.log
/Users/mac/bin/litellm-metrics-summary
curl -sS http://127.0.0.1:8787/api/summary | jq '{totals, states}'
```

3. Preserve protocol shape:

- Do not turn a Responses provider into `chat/completions` merely because NVIDIA uses chat completions; switch only after verifying that the upstream rejects valid `previous_response_id` and supports `/chat/completions`.
- Do not globally drop `previous_response_id`; only add known-incompatible models to the callback's drop list.
- Do not assume one endpoint URL, model name, or key variable for all OpenAI Compatibility providers.

4. Restart and validate after edits:

```bash
python3 -m py_compile /Users/mac/copilot_compat_callbacks.py
zsh -n /Users/mac/start-litellm-nvidia.sh
launchctl kickstart -k "gui/$(id -u)/com.inchheart.litellm-nvidia"
sleep 8
curl -sS http://127.0.0.1:4000/v1/models | jq '{count:(.data|length)}'
curl -sS http://127.0.0.1:8787/api/summary | jq '{totals, states}'
```

5. Update the Obsidian note when the fix becomes part of the working method:

`/Users/mac/Library/Mobile Documents/iCloud~md~obsidian/Documents/笔记本/寸心/项目规划与方案/LiteLLM NVIDIA 多账号路由方案.md`

## Naming

Use **OpenAI Compatibility** as the generic provider name for non-NVIDIA OpenAI-compatible relay endpoints. Avoid hard-coding "GBox" in user-facing docs, skills, or VS Code provider labels unless the user explicitly asks to track that vendor name.

For provider key variables, prefer stable generic names:

| Case | Variable pattern |
| --- | --- |
| Single generic relay | `OPENAI_COMPATIBILITY_API_KEY` |
| Multiple generic relays | `OPENAI_COMPATIBILITY_<SLUG>_API_KEY` |
| NVIDIA multi-key | `NVIDIA_API_KEY_1` ... `NVIDIA_API_KEY_10` |
