# OpenAI Compatibility Providers

## Purpose

Use **OpenAI Compatibility** as the generic name for non-NVIDIA relay endpoints whose base URL, model name, key, and protocol may change over time.

Do not hard-code a vendor name such as GBox in reusable instructions. Ask for or inspect:

| Required fact | Example |
| --- | --- |
| API base URL | `https://example-relay.test/v1` |
| API key | Store locally only; do not print |
| Model name | `gpt-5.5`, `claude-*`, etc. |
| Protocol | `responses` or `chat-completions` |
| Unsupported params | e.g. `previous_response_id` |

## VS Code Mapping

Responses provider, only when the upstream really supports Responses continuation:

```json
{
  "name": "OpenAI Compatibility",
  "vendor": "customendpoint",
  "apiKey": "sk-litellm-local",
  "apiType": "responses",
  "models": [
    {
      "id": "gpt-5.5",
      "name": "gpt-5.5",
      "url": "http://127.0.0.1:4000/v1",
      "toolCalling": true,
      "vision": true,
      "maxInputTokens": 256000,
      "maxOutputTokens": 16000
    }
  ]
}
```

Chat completions provider, recommended when the upstream rejects `previous_response_id` but `/chat/completions` works:

```json
{
  "name": "OpenAI Compatibility",
  "vendor": "customendpoint",
  "apiKey": "sk-litellm-local",
  "apiType": "chat-completions",
  "models": [
    {
      "id": "gpt-5.5",
      "name": "gpt-5.5",
      "url": "http://127.0.0.1:4000/v1/chat/completions",
      "toolCalling": true,
      "vision": true,
      "maxInputTokens": 256000,
      "maxOutputTokens": 16000
    }
  ]
}
```

## LiteLLM Mapping

Use a provider-specific environment variable. For a single generic relay:

```yaml
model_list:
  - model_name: gpt-5.5
    litellm_params:
      model: openai/gpt-5.5
      api_base: https://example-relay.test/v1
      api_key: os.environ/OPENAI_COMPATIBILITY_API_KEY
      cooldown_time: 0
    model_info:
      id: openai_compatibility_gpt_5_5

environment_variables:
  OPENAI_COMPATIBILITY_API_KEY: <real key>
```

Ensure `/Users/mac/start-litellm-nvidia.sh` loads the same variable:

```zsh
load_config_env_var OPENAI_COMPATIBILITY_API_KEY
```

For multiple relay providers, use a slugged variable:

```yaml
api_key: os.environ/OPENAI_COMPATIBILITY_<SLUG>_API_KEY
```

## Responses API Caveat

Some relay endpoints claim Responses API support but reject Copilot parameters:

```text
Unsupported parameter: previous_response_id
```

First test whether the endpoint supports a real `previous_response_id`. A fake id is not enough.

1. Send a first `/v1/responses` request with `store: true`.
2. Capture the returned `id`.
3. Send a second `/v1/responses` request with that real `previous_response_id`.
4. If it still returns `Unsupported parameter: previous_response_id`, the endpoint has incomplete Responses state support.

If `/chat/completions` succeeds, switch the VS Code model to `chat-completions` instead of trying to emulate Responses state:

```json
{
  "name": "OpenAI Compatibility",
  "vendor": "customendpoint",
  "apiKey": "sk-litellm-local",
  "apiType": "chat-completions",
  "models": [
    {
      "id": "gpt-5.5",
      "name": "gpt-5.5",
      "url": "http://127.0.0.1:4000/v1/chat/completions",
      "toolCalling": true,
      "vision": true,
      "maxInputTokens": 256000,
      "maxOutputTokens": 16000
    }
  ]
}
```

Keep `DROP_PREVIOUS_RESPONSE_ID_MODELS` narrow and defensive. It should not turn a request containing only `previous_response_id` into a request with no `input`, `prompt`, or `conversation_id`.

Chat-completions smoke test:

```bash
curl -sS --max-time 120 http://127.0.0.1:4000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer sk-litellm-local' \
  -d '{"model":"gpt-5.5","messages":[{"role":"user","content":"只回复 ok"}],"max_tokens":32}' \
  | jq '{model, content:.choices[0].message.content, finish_reason:.choices[0].finish_reason, error}'
```

If the provider truly supports Responses, keep VS Code `apiType: responses`:

1. Keep VS Code `apiType: responses`.
2. Route VS Code to `http://127.0.0.1:4000/v1`.
3. Add the exact incompatible model to `DROP_PREVIOUS_RESPONSE_ID_MODELS` in `copilot_compat_callbacks.py`.
4. Test both non-streaming and streaming `/v1/responses`.

Test:

```bash
curl -sS --max-time 120 http://127.0.0.1:4000/v1/responses \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer sk-litellm-local' \
  -d '{"model":"gpt-5.5","input":"只回复 ok","previous_response_id":"resp_fake","max_output_tokens":32}'
```

Streaming test:

```bash
curl -sS --max-time 120 http://127.0.0.1:4000/v1/responses \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer sk-litellm-local' \
  -d '{"model":"gpt-5.5","input":"只回复 ok","previous_response_id":"resp_fake","max_output_tokens":32,"stream":true}' \
  | head -n 30
```

Look for `response.output_text.delta`.
