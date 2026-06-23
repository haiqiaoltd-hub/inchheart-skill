# New API

Use this reference for New API channel setup, groups, registration defaults, request passthrough, model list handling, logo/SMTP, and compatibility transforms.

## Current Shape

| Field | Value |
| --- | --- |
| Deploy path | `/opt/new-api-native` |
| Service | `new-api-native.service` |
| Binary | `/opt/new-api-native/new-api` |
| Database | SQLite at `/opt/new-api-native/data/one-api.db` |
| Listen port | `8090` |
| Public URL | `https://api.eastart.asia` |
| Reverse proxy | Caddy to `127.0.0.1:8090` |
| Version observed | `v1.0.0-rc.14` |
| Redis/PostgreSQL | Disabled |

Useful checks:

```bash
sudo systemctl status new-api-native --no-pager -l
sudo journalctl -u new-api-native -n 120 --no-pager
curl -sSI --max-time 8 http://127.0.0.1:8090/ | grep -i 'HTTP/\|X-New-Api-Version'
sudo ls -lh /opt/new-api-native/data/one-api.db
```

Do not print `SESSION_SECRET`, channel keys, token keys, user passwords, access tokens, or raw env files.

## Operating Preference

- Treat New API as the public model configuration and token site for `api.eastart.asia`.
- Treat server LiteLLM as the source of truth for upstream NVIDIA routing and key fan-out.
- Do not update New API channel model lists or database `channels.models` automatically unless the user explicitly asks. The user often maintains New API model lists manually in the UI.
- Request passthrough may be enabled when clients such as CC Switch, Claude/Codex-compatible tools, OpenCode, OpenClaw, or other OpenAI-compatible clients already send the final desired request shape.

## LiteLLM Channel

New API channel configuration for the local server LiteLLM proxy:

| Field | Value |
| --- | --- |
| Base URL in UI | `http://127.0.0.1:4000` |
| Effective API root | `http://127.0.0.1:4000/v1` |
| Channel type | OpenAI-compatible |
| Key | LiteLLM currently has no master key; use a placeholder only if New API requires a value |

Keep New API model lists aligned only when the user asks. Otherwise, report the LiteLLM `/v1/models` list and let the user choose which models to expose in New API.

## Non-Image Model Compatibility

For text-only or non-image-generation models, use New API request parameter compatibility to remove image-generation tools sent by clients. Add this JSON in the New API channel/model request parameter or advanced custom parameter field:

```json
{
  "operations": [
    {
      "path": "tools",
      "mode": "prune_objects",
      "value": {
        "where": {
          "type": "image_generation"
        }
      }
    },
    {
      "path": "tools",
      "mode": "prune_objects",
      "value": {
        "where": {
          "type": "image_generation_call"
        }
      }
    }
  ]
}
```

This only removes unsupported image-generation tool declarations from outgoing requests. It does not add image generation capability to a model.

Use it when a text model or relay fails because a client advertises `image_generation` or `image_generation_call` tools.

## Database Caution

Prefer UI changes for New API settings. If the user explicitly asks for database edits, back up first:

```bash
ts="$(date +%Y%m%d-%H%M%S)"
sudo cp /opt/new-api-native/data/one-api.db "/opt/new-api-native/data/one-api.db.bak.$ts"
```

Use Python `sqlite3` if the server lacks the `sqlite3` CLI. Never display secret-bearing columns unless redacted.
