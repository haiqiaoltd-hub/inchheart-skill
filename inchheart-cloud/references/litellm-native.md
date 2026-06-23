# Server LiteLLM

Use this reference for the server-side LiteLLM proxy, NVIDIA NIM model routing, multi-key fan-out, callbacks, rate limits, embeddings, and VS Code/OpenAI-compatible client model lists.

## Current Shape

| Field | Value |
| --- | --- |
| Deploy path | `/opt/litellm-native` |
| Service | `litellm-native.service` |
| Config | `/opt/litellm-native/config.yaml` |
| Callback | `/opt/litellm-native/copilot_compat_callbacks.py` |
| Env file | `/etc/litellm-native.env` |
| Python env | `/opt/litellm-native/venv` |
| Listen port | `127.0.0.1:4000` |
| NVIDIA endpoint | `https://integrate.api.nvidia.com/v1` |
| Router | `simple-shuffle`, weighted failover, `rpm: 20` per deployment, `cooldown_time: 3600` |

NVIDIA keys are stored as `NVIDIA_API_KEY_1` ... `NVIDIA_API_KEY_10` in `/etc/litellm-native.env`. Do not print them.

This file is the source of truth for server LiteLLM compatibility notes: Copilot compatibility, NVIDIA multi-account routing, RPM limits, 429/cooldown policy, callback behavior, and model smoke tests.

## Service Checks

```bash
sudo systemctl status litellm-native --no-pager -l
sudo journalctl -u litellm-native -n 120 --no-pager
sudo ss -lntp | grep -E ':4000\b' || true
curl -sS --max-time 10 http://127.0.0.1:4000/v1/models | jq '{count:(.data|length), models:[.data[].id]}'
```

Smoke test chat:

```bash
curl -sS --max-time 70 http://127.0.0.1:4000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"z-ai/glm-5.1","messages":[{"role":"user","content":"Reply OK only."}],"max_tokens":8,"stream":false}' \
  | jq '{model, content:(.choices[0].message.content // null), error:(.error // null)}'
```

Smoke test embeddings:

```bash
curl -sS --max-time 70 http://127.0.0.1:4000/v1/embeddings \
  -H 'Content-Type: application/json' \
  -d '{"model":"baai/bge-m3","input":"hello world"}' \
  | jq '{model:(.model // null), object:(.object // null), dim:((.data[0].embedding // []) | length), error:(.error // null)}'
```

## Model Group Pattern

Expose one model name while routing across multiple NVIDIA keys:

```yaml
- model_name: z-ai/glm-5.1
  litellm_params:
    model: openai/z-ai/glm-5.1
    api_base: https://integrate.api.nvidia.com/v1
    api_key: os.environ/NVIDIA_API_KEY_1
  rpm: 20
  model_info:
    id: nvidia_z_ai_glm_5_1_key1
```

Repeat each model for keys 1 through 10 with unique `model_info.id`.

Use repeated `model_name` values and unique deployment IDs:

```text
Client model: qwen/qwen3.5-397b-a17b
LiteLLM deployment 1: qwen/qwen3.5-397b-a17b + NVIDIA_API_KEY_1
LiteLLM deployment 2: qwen/qwen3.5-397b-a17b + NVIDIA_API_KEY_2
...
LiteLLM deployment 10: qwen/qwen3.5-397b-a17b + NVIDIA_API_KEY_10
```

Do not switch to round-robin merely for speed. Prior tests did not show a stable speed win from fixed-key or rotating-key routing; NVIDIA free endpoint latency varies more than any likely cache benefit.

Embedding models such as `baai/bge-m3` must use the embeddings endpoint and should be marked as embedding in `model_info` when needed:

```yaml
model_info:
  id: nvidia_baai_bge_m3_key1
  mode: embedding
```

## Editing Workflow

Back up before editing:

```bash
ts="$(date +%Y%m%d-%H%M%S)"
sudo cp /opt/litellm-native/config.yaml "/opt/litellm-native/config.yaml.bak.$ts"
sudo cp /opt/litellm-native/copilot_compat_callbacks.py "/opt/litellm-native/copilot_compat_callbacks.py.bak.$ts"
```

After editing:

```bash
sudo /opt/litellm-native/venv/bin/python -m py_compile /opt/litellm-native/copilot_compat_callbacks.py
sudo systemctl restart litellm-native
sleep 16
systemctl is-active litellm-native
curl -sS --max-time 10 http://127.0.0.1:4000/v1/models | jq '{count:(.data|length)}'
```

On this small GCP host, LiteLLM may need more than 10 seconds to listen after restart when many deployments are configured.

## Callback Responsibilities

The server callback handles compatibility for Copilot-style and OpenAI-compatible clients:

- Clamp output token budgets for chat models so tiny client defaults do not trigger `Response too long` or premature truncation.
- Sanitize tool schemas with missing or non-string descriptions.
- Convert Anthropic-style tool use/results to OpenAI function tool calls where needed.
- Convert `description: null` to `description: ""` and `parameters: null` to `{"type":"object","properties":{}}` for strict upstream providers.
- Coerce `finish_reason: length` to `stop` for clients that treat length as failure.
- Drop `previous_response_id` only for known-incompatible models; do not remove it globally because real Responses implementations use it for continuity.
- Skip output-token budget rewriting for embedding models such as `baai/bge-m3`; NVIDIA embeddings rejects `max_output_tokens`.

Do not add image-generation compatibility here when New API request parameter pruning can solve it at the public channel layer.

### Output Budget

Chat Completions uses `max_tokens`; Responses uses `max_output_tokens`. The configured pair means:

| Pair position | Meaning |
| --- | --- |
| First value | Minimum requested output ceiling |
| Second value | Maximum requested output ceiling |

This does not force the model to output that many tokens. It only changes the allowed maximum for the request.

Use lower budgets for models known to hang, stream slowly, or produce bad long outputs. Use higher budgets for stable coding/reasoning models.

### Tool Schema Sanitizer

Copilot and some Claude-compatible clients may send invalid tool definitions:

```json
{
  "type": "function",
  "function": {
    "name": "read_file",
    "description": null,
    "parameters": null
  }
}
```

Sanitize to:

```json
{
  "type": "function",
  "function": {
    "name": "read_file",
    "description": "",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  }
}
```

Do not invent tool meanings. Empty string is safer than a misleading description.

### Anthropic Tool Compatibility

Some clients send Anthropic-style `tool_use` / `tool_result` content blocks even when the final upstream is OpenAI-compatible chat completions. The server callback may convert those into OpenAI `tool_calls` / `tool` messages so direct clients such as OpenCode, OpenClaw, or other CLI tools can work without CC Switch doing all conversion.

Keep this conversion scoped to request-shape compatibility. Do not add model-specific semantic behavior in the callback.

### Responses Parameter Sanitizer

Only drop unsupported Responses parameters for known incompatible models:

```python
DROP_PREVIOUS_RESPONSE_ID_MODELS = {
    "gpt-5.5",
}
```

Do not globally remove `previous_response_id`. If a provider rejects a valid `previous_response_id` but supports chat completions, prefer exposing that provider as `chat-completions`.

## Rate Limits

Observed NVIDIA free endpoint behavior:

| Constraint | Observation |
| --- | --- |
| Limit dimension | Account + model |
| Common limit | About `40 RPM` per account per model |
| Conservative configured limit | `20 RPM` per deployment |
| Cooldown policy | `cooldown_time: 3600` because triggering 429 can freeze a key for a long time |
| Failure shape | `429`, `ResourceExhausted`, worker-busy responses, or hidden upstream throttling |

The goal is to avoid triggering upstream 429s, not to maximize burst rate.

Use per-deployment `rpm: 20` as the conservative default. The user prefers not triggering 429 at all because once a key enters cooldown it can effectively freeze that deployment for about an hour.

Only enable strict pre-call checks if needed:

```yaml
router_settings:
  optional_pre_call_checks:
    - enforce_model_rate_limits
```

This can return local 429s before calling NVIDIA. It is useful when protecting keys matters more than client-side convenience.

## Troubleshooting

| Symptom | Likely cause | First fix |
| --- | --- | --- |
| `Response too long` | Tiny client output budget or `finish_reason: length` | Confirm callback is loaded; inspect output budget and finish-reason rewrite |
| `ToolDescription description ... NoneType` | Tool schema contains `description: null` | Confirm tool schema sanitizer runs before upstream |
| `Unsupported parameter: previous_response_id` | Provider lacks full Responses state support | Drop only for that model or expose as `chat-completions` after testing |
| `401 Invalid token` | Wrong key, placeholder key, or env not loaded | Verify key variable reference and service env loading without printing secrets |
| `429` on NVIDIA | Upstream account+model rate limit or cooldown | Keep multi-key routing, `rpm: 20`, and one-hour cooldown; reduce concurrency |
| `ResourceExhausted: All workers are busy` | NVIDIA worker pool overloaded | Wait, switch model, or lower concurrency; adding keys may not help |
| `MidStreamFallbackError` or socket timeout | Long output or unstable stream | Lower per-model output budget or use faster model |
| Embedding request rejects `max_output_tokens` | Callback treated embedding like chat | Add model to embedding skip logic and test `/v1/embeddings` |

Log search:

```bash
sudo journalctl -u litellm-native -n 300 --no-pager | \
  rg "Response too long|ToolDescription|previous_response_id|Invalid token|429|ResourceExhausted|MidStreamFallback|Timeout|All workers|max_output_tokens"
```

When checking direct request behavior, prefer minimal smoke tests before larger agent workflows.

## VS Code Model Lists

Local VS Code custom models live at:

```text
/Users/mac/Library/Application Support/Code/User/chatLanguageModels.json
```

When updating the `小橘中转站` provider for `https://api.eastart.asia/v1`, include only chat models. Do not add embedding models such as `baai/bge-m3` to VS Code chat model lists.

Back up before editing:

```bash
ts="$(date +%Y%m%d-%H%M%S)"
cp "/Users/mac/Library/Application Support/Code/User/chatLanguageModels.json" \
  "/Users/mac/Library/Application Support/Code/User/chatLanguageModels.json.bak.$ts"
```

## Boundaries

- Do not modify New API channel model lists unless the user explicitly asks.
- Do not modify the old Mac local LiteLLM files unless the user explicitly asks about local LiteLLM.
- Keep server LiteLLM as the source of truth for upstream NVIDIA routing.
