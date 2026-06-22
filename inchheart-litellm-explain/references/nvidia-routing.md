# NVIDIA Multi-Account Routing

## Goal

NVIDIA Build/NIM endpoint:

```text
https://integrate.api.nvidia.com/v1
```

Expose one public model name to clients while LiteLLM routes to many deployments with different NVIDIA API keys.

```text
Client model: qwen/qwen3.5-397b-a17b
LiteLLM deployments:
  qwen/qwen3.5-397b-a17b + NVIDIA_API_KEY_1
  qwen/qwen3.5-397b-a17b + NVIDIA_API_KEY_2
  ...
```

## Model Group Pattern

Use repeated `model_name` values and unique `model_info.id` values:

```yaml
model_list:
  - model_name: qwen/qwen3.5-397b-a17b
    litellm_params:
      model: openai/qwen/qwen3.5-397b-a17b
      api_base: https://integrate.api.nvidia.com/v1
      api_key: os.environ/NVIDIA_API_KEY_1
    model_info:
      id: nvidia_qwen_qwen3_5_397b_a17b_key1

  - model_name: qwen/qwen3.5-397b-a17b
    litellm_params:
      model: openai/qwen/qwen3.5-397b-a17b
      api_base: https://integrate.api.nvidia.com/v1
      api_key: os.environ/NVIDIA_API_KEY_2
    model_info:
      id: nvidia_qwen_qwen3_5_397b_a17b_key2
```

## Router Settings

Current working base:

```yaml
router_settings:
  routing_strategy: simple-shuffle
  enable_weighted_failover: true
  num_retries: 2
  allowed_fails: 0
  cooldown_time: 65
  retry_after: 1
```

| Setting | Meaning |
| --- | --- |
| `simple-shuffle` | Low-overhead random selection across equivalent deployments |
| `enable_weighted_failover` | Retry another deployment in the same model group |
| `allowed_fails: 0` | Cool down a failed deployment immediately |
| `cooldown_time: 65` | NVIDIA 429 often recovers after about 1 minute |

Do not switch to round-robin merely for speed. Tests showed fixed-key or rotating-key routing did not produce a stable speed win; NVIDIA free endpoints vary more than any likely cache benefit.

## Rate Limits

Observed NVIDIA free endpoint behavior:

| Constraint | Observation |
| --- | --- |
| Limit dimension | Account + model |
| Common limit | About `40 RPM` per account per model |
| Failure | `429`, sometimes worker-busy or hidden upstream constraints |
| Cooldown | About 1 minute |

If random multi-key routing still hits frequent 429, add per-deployment `rpm: 40`. Treat this as respecting the upstream limit, not bypassing it:

```yaml
- model_name: qwen/qwen3.5-397b-a17b
  litellm_params:
    model: openai/qwen/qwen3.5-397b-a17b
    api_base: https://integrate.api.nvidia.com/v1
    api_key: os.environ/NVIDIA_API_KEY_1
  rpm: 40
```

Only enable strict pre-call checks if needed:

```yaml
router_settings:
  optional_pre_call_checks:
    - enforce_model_rate_limits
```

This can return local 429s instead of waiting for NVIDIA.

