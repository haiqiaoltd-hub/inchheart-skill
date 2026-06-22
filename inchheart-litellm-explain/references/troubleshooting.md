# Troubleshooting

## Error Map

| Symptom | Cause | Fix |
| --- | --- | --- |
| `Response too long` | Copilot dislikes `finish_reason: length` or small output budget | Ensure callback is loaded; check output budget and finish reason rewrite |
| `ToolDescription description ... NoneType` | Tool schema has `description: null` | Enable tool schema sanitizer |
| `Unsupported parameter: previous_response_id` | Relay endpoint lacks full Responses state support | Test with a real response id; if it still fails and chat works, switch provider to `chat-completions` |
| `401 Invalid token` | Key wrong, placeholder copied, or start script did not load env var | Verify config has real key and start script loads variable; do not print full key |
| `429` after one 502 on a single-deployment relay | LiteLLM cooled down the only deployment | Set deployment-level `cooldown_time: 0` for that single relay model |
| `429` on NVIDIA | Upstream rate limit | Use multi-key routing, cooldown, optional `rpm` |
| `ResourceExhausted: All workers are busy` | Upstream worker pool overloaded | Wait, switch model, or lower concurrency; keys may not help |
| `MidStreamFallbackError` / socket timeout | Long output or unstable model stream | Lower per-model output budget or use faster model |
| Non-streaming `output_text` is null but `output[].content[].text` exists | LiteLLM Responses aggregation gap | Check raw `output`; stream may still be fine for Copilot |

## Log Search

```bash
rg -n "Response too long|ToolDescription|previous_response_id|Invalid token|429|ResourceExhausted|MidStreamFallback|Timeout|All workers" \
  /Users/mac/litellm.err.log /Users/mac/litellm.log
```

## Direct Smoke Tests

Chat completions:

```bash
curl -sS --max-time 90 http://127.0.0.1:4000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer sk-litellm-local' \
  -d '{"model":"qwen/qwen3.5-397b-a17b","messages":[{"role":"user","content":"只回复 ok"}],"max_tokens":32}' \
  | jq '{model, content:.choices[0].message.content, finish_reason:.choices[0].finish_reason, error}'
```

Responses, basic smoke test without continuation:

```bash
curl -sS --max-time 120 http://127.0.0.1:4000/v1/responses \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer sk-litellm-local' \
  -d '{"model":"gpt-5.5","input":"只回复 ok","store":true,"max_output_tokens":32}' \
  | jq '{id, model, output, output_text, status, error}'
```

Responses continuation test, use a real response id:

```bash
first_id="$(
  curl -sS --max-time 120 http://127.0.0.1:4000/v1/responses \
    -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer sk-litellm-local' \
    -d '{"model":"gpt-5.5","input":"只回复 first","store":true,"max_output_tokens":32}' \
  | jq -r '.id'
)"

curl -sS --max-time 120 http://127.0.0.1:4000/v1/responses \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer sk-litellm-local' \
  -d "{\"model\":\"gpt-5.5\",\"input\":\"只回复 second\",\"previous_response_id\":\"$first_id\",\"max_output_tokens\":32}" \
  | jq '{id, model, output, output_text, status, error}'
```

OpenAI Compatibility chat-completions:

```bash
curl -sS --max-time 120 http://127.0.0.1:4000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer sk-litellm-local' \
  -d '{"model":"gpt-5.5","messages":[{"role":"user","content":"只回复 ok"}],"max_tokens":32}' \
  | jq '{model, content:.choices[0].message.content, finish_reason:.choices[0].finish_reason, error}'
```

Streaming Responses:

```bash
curl -sS --max-time 120 http://127.0.0.1:4000/v1/responses \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer sk-litellm-local' \
  -d '{"model":"gpt-5.5","input":"只回复 ok","max_output_tokens":32,"stream":true}' \
  | head -n 30
```

## VS Code Reload

After editing `chatLanguageModels.json`, tell the user to run:

```text
Developer: Reload Window
```

in VS Code so Copilot reloads custom model configuration.
