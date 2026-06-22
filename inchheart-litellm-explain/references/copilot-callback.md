# Copilot Compatibility Callback

Callback file:

`/Users/mac/copilot_compat_callbacks.py`

LiteLLM config must include:

```yaml
litellm_settings:
  drop_params: true
  request_timeout: 120
  callbacks: copilot_compat_callbacks.proxy_handler_instance
```

## Responsibilities

| Function | Why |
| --- | --- |
| Output budget clamping | Prevent tiny Copilot `max_tokens` values from causing `Response too long` |
| `finish_reason: length` -> `stop` | Copilot often treats `length` as a hard failure |
| Tool schema sanitizer | Fix `description: null` and `parameters: null` before strict providers reject them |
| Responses parameter sanitizer | Drop known-unsupported params such as `previous_response_id` for specific models only |

## Output Budget

Chat Completions uses `max_tokens`.

Responses API uses `max_output_tokens`.

Current pattern:

```python
MODEL_OUTPUT_BUDGETS = {
    "qwen/qwen3.5-397b-a17b": (16384, 32768),
    "stepfun-ai/step-3.7-flash": (16384, 32768),
    "minimaxai/minimax-m3": (8192, 16384),
    "openai/gpt-oss-120b": (4096, 8192),
    "gpt-5.5": (8192, 16000),
}
```

Meaning:

| Pair | Meaning |
| --- | --- |
| First value | Minimum requested output ceiling |
| Second value | Maximum requested output ceiling |

It does not force the model to output that many tokens; it only changes the allowed maximum for that request.

## Tool Schema Sanitizer

Copilot may send:

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

Strict providers may reject this. Sanitize to:

```json
{
  "type": "function",
  "function": {
    "name": "read_file",
    "description": "",
    "parameters": {"type": "object", "properties": {}}
  }
}
```

Do not invent tool meanings. Empty string is safer than a misleading description.

## Responses Parameter Sanitizer

Only drop unsupported Responses parameters for known incompatible models:

```python
DROP_PREVIOUS_RESPONSE_ID_MODELS = {
    "gpt-5.5",
}
```

Do not globally remove `previous_response_id`; full Responses implementations use it for conversation continuity.

## Local Unit Test Pattern

Use this shape after callback edits:

```bash
PYTHONPATH=/Users/mac/.local/share/uv/tools/litellm/lib/python3.12/site-packages python3 - <<'PY'
import asyncio, importlib.util
from pathlib import Path

path = Path('/Users/mac/copilot_compat_callbacks.py')
spec = importlib.util.spec_from_file_location('copilot_compat_callbacks', path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

async def main():
    data = {
        'model': 'gpt-5.5',
        'input': '只回复 ok',
        'max_output_tokens': 32000,
        'previous_response_id': 'resp_fake',
        'tools': [{'type': 'function', 'name': 'dummy', 'description': None, 'parameters': None}],
    }
    out = await mod.proxy_handler_instance.async_pre_call_hook(None, None, data, 'responses')
    assert 'previous_response_id' not in out
    assert out['max_output_tokens'] <= 16000
    assert out['tools'][0]['description'] == ''
    assert out['tools'][0]['parameters']['type'] == 'object'
    print('callback test passed')

asyncio.run(main())
PY
```

