# Observability

Use this reference for Heart's LiteLLM redacted request metrics, slow-request statistics, and model health panel.

## Files

| Path | Purpose |
| --- | --- |
| `/Users/mac/litellm_request_metrics.jsonl` | One redacted JSON event for each real LiteLLM success/failure request |
| `/Users/mac/litellm_slow_requests.jsonl` | Requests slower than the callback threshold plus failures |
| `/Users/mac/litellm_health_probes.jsonl` | Active health probe results |
| `/Users/mac/bin/litellm-metrics-summary` | CLI summary for request metrics |
| `/Users/mac/bin/litellm-health-panel` | Local HTTP health dashboard service |
| `/Users/mac/bin/litellm-health-probe` | Manual health probe CLI |
| `/Users/mac/Library/LaunchAgents/com.inchheart.litellm-health-panel.plist` | LaunchAgent for the health panel |
| `/Users/mac/litellm-health-panel.log` | Health panel stdout |
| `/Users/mac/litellm-health-panel.err.log` | Health panel stderr |

## Redacted Request Metrics

Metrics are written by `/Users/mac/copilot_compat_callbacks.py` through LiteLLM's `async_log_success_event` and `async_log_failure_event`.

The callback records metadata only:

| Field type | Examples |
| --- | --- |
| Safe request metadata | `model`, `api_base`, `call_type`, `stream`, `max_tokens`, `max_output_tokens` |
| Timing | `duration_ms`, `slow`, `slow_threshold_ms` |
| Outcome | `status`, `finish_reason`, `error.type`, `error.status_code` |
| Usage | `prompt_tokens`, `completion_tokens`, `total_tokens` when provided by the upstream |

Do not add prompt text, response text, request bodies, API keys, `Authorization` headers, or raw provider payloads to these logs.

Default slow threshold:

```text
COPILOT_COMPAT_SLOW_REQUEST_MS=30000
```

Default paths:

```text
COPILOT_COMPAT_METRICS_LOG_PATH=~/litellm_request_metrics.jsonl
COPILOT_COMPAT_SLOW_LOG_PATH=~/litellm_slow_requests.jsonl
```

The service currently runs with `HOME=/Users/mac`, so these expand to `/Users/mac/...`.

Useful commands:

```bash
/Users/mac/bin/litellm-metrics-summary
tail -n 20 /Users/mac/litellm_request_metrics.jsonl | jq -c '.'
tail -n 20 /Users/mac/litellm_slow_requests.jsonl | jq -c '.'
rg -n 'nvapi-|sk-[A-Za-z0-9_-]{8,}|Bearer [A-Za-z0-9._~+/-]+' \
  /Users/mac/litellm_request_metrics.jsonl /Users/mac/litellm_slow_requests.jsonl
```

## Health Panel

Local dashboard:

```text
http://127.0.0.1:8787
```

API:

```bash
curl -sS http://127.0.0.1:8787/api/summary | jq '{totals, states}'
curl -sS http://127.0.0.1:8787/api/probe/latest | jq '.recent[-5:]'
curl -sS -X POST http://127.0.0.1:8787/api/probe/run | jq '{models, healthy, degraded, slow, down}'
```

Service checks:

```bash
launchctl print "gui/$(id -u)/com.inchheart.litellm-health-panel" | rg "state =|pid =|last exit code"
lsof -nP -iTCP:8787 -sTCP:LISTEN
tail -n 80 /Users/mac/litellm-health-panel.err.log /Users/mac/litellm-health-panel.log
```

Restart:

```bash
python3 -m py_compile /Users/mac/bin/litellm-health-panel
launchctl kickstart -k "gui/$(id -u)/com.inchheart.litellm-health-panel"
sleep 3
curl -sS http://127.0.0.1:8787/api/summary | jq '{totals, states}'
```

## Active Probe Behavior

The health probe calls the local LiteLLM proxy, not upstream providers directly:

```text
http://127.0.0.1:4000/v1/chat/completions
```

It probes visible model groups, not every deployment/key. With the current NVIDIA setup this means roughly 19 requests per full probe, not 181 requests.

Probe requests include:

```json
{"metadata":{"inchheart_health_probe":true}}
```

The callback must use that marker to:

| Behavior | Why |
| --- | --- |
| Skip output budget clamping | Keep probe `max_tokens` small |
| Skip passive request metrics logging | Avoid polluting real usage metrics |

Current probe defaults:

| Variable | Default |
| --- | --- |
| `LITELLM_HEALTH_PROBE_TIMEOUT` | `35` seconds |
| `LITELLM_HEALTH_PROBE_CONCURRENCY` | `2` |
| `LITELLM_HEALTH_PROBE_MAX_MODELS` | `0` meaning all visible models |
| `LITELLM_HEALTH_PROBE_MAX_TOKENS` | `32` |
| `LITELLM_HEALTHY_MS` | `15000` |
| `LITELLM_DEGRADED_MS` | `30000` |

Manual run:

```bash
/Users/mac/bin/litellm-health-probe
```

Interpretation:

| State | Meaning |
| --- | --- |
| `healthy` | HTTP 200 with a valid `choices` response and duration <= `LITELLM_HEALTHY_MS` |
| `degraded` | Valid response but slower than healthy threshold |
| `slow` | Valid response but slower than degraded threshold |
| `down` | Timeout, connection error, HTTP error, or malformed response |
| `unknown` | No probe record yet |

The probe is intentionally conservative. A model marked `down` may still work later; it means the short local LiteLLM check failed in the most recent run.

## Current Known Shape

As of the health panel implementation:

| Item | Value |
| --- | --- |
| Panel URL | `http://127.0.0.1:8787` |
| LiteLLM proxy | `http://127.0.0.1:4000/v1` |
| Probe mode | Chat Completions only |
| Probe scope | Visible model groups |
| Probe log | `/Users/mac/litellm_health_probes.jsonl` |

Do not enable automatic high-frequency probes without considering NVIDIA's free endpoint rate limits.
